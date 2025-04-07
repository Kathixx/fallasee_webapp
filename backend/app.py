from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import mlflow.sklearn
from flask import session
from datetime import timedelta
import mlflow.pytorch

import numpy as np


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from mlflow.sklearn import save_model

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder

import sentencepiece
import os

from torch.utils.data import Dataset, DataLoader
import torch

from transformers import TrainingArguments, Trainer, AutoModelForSequenceClassification, AutoModel, AutoTokenizer, AutoConfig
 

# SECRET KEY
# TODO: SAFE IN ENVIRONMENT VARIABLE
import secrets
secret_key = secrets.token_hex(32)  # 64-character hexadecimal string


app = Flask(__name__)
app.secret_key = secret_key  # Replace with actual key
app.config.update(
    PERMANENT_SESSION_LIFETIME= timedelta(minutes=30),
    SESSION_COOKIE_SECURE=False, # only with HTTPS
    SESSION_COOKIE_SAMESITE='Lax',  # Allows cross-origin cookies
    SESSION_COOKIE_HTTPONLY=False,
    SESSION_COOKIE_PATH='/',
)

CORS(app, resources={
    r"/predict": {
        "origins": "http://localhost:5173",
        "methods": ["POST","GET" "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True 
    }
})


tokenizer = AutoTokenizer.from_pretrained('microsoft/deberta-v3-base', use_fast=False)

def tokenize(texts):
    return tokenizer(
        texts,
        padding="max_length", #ensures that all tokenized sequences are padded to the same length, padding adds special tokens to shorter sequeces so they match the maximum length
        truncation=True, #if sequence exceeds max, it will be trucated
        max_length=512, #for most transformer models, 512 is a common limit for maximum length
        return_tensors="pt" #converts the output to pytorch tensors
    )

def predict(model, encodings, batch_size=8):
    # Set the model to evaluation mode
    model.eval()
    
    # Use GPU
    device = torch.device("mps")
    model.to(device)
    
    # Perform inference
    probabilities = []
    for i in range(0, len(encodings["input_ids"]), batch_size):
        with torch.no_grad():
            batch = {
                "input_ids": encodings["input_ids"][i:i+batch_size].to(device),
                "attention_mask": encodings["attention_mask"][i:i+batch_size].to(device)
            }
            outputs = model(**batch)
            probs = torch.softmax(outputs.logits, dim=-1).cpu().numpy()
            probabilities.extend(probs)
            
        # Clear GPU memory after each batch
        torch.mps.empty_cache()
    
    return np.array(probabilities)

def get_label(label):
    if label == 0:
        return 'ad_hominem'
    if label == 1:
        return 'appeal to authority'
    if label == 2:
        return 'appeal to emotion'
    if label == 3:
        return 'false dilemma'
    if label == 4:
        return 'faulty generalization'
    if label == 5:
        return 'none'

def get_first_prediction(proba):
    pred = np.argmax(proba, axis=1)
    pred_int = int(pred[0])
    proba = proba[np.arange(len(pred)), pred]
    proba_int = float(proba[0])
    return pred_int, proba_int

def get_second_prediction(proba):
    pred = np.argsort(proba, axis=1)[:, -2] 
    pred_int = int(pred[0])
    proba = np.sort(proba, axis=1)[:, -2]
    proba_int = float(proba[0])
    return pred_int, proba_int

@app.route("/")
def hello():
    return "Hello from Flask!"

@app.after_request
def after_request(response):
    # Add CORS headers for every response
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'  # Replace with your client domain
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response

# source: https://heartbeat.comet.ml/deploying-a-text-classification-model-using-flask-and-vue-js-25b9aa7ff048
# The input_predict_text() function receives the text input from the web application, and using the text
# classifier (best-model.pt) loaded from the models folder, predicts and returns the result in Json format.
# The get_results function, on the other hand, prepares the output to be displayed on the Vue.js frontend.

@app.route('/predict', methods=['GET'])
@cross_origin(origin='http://localhost:5173')
def get_result():
    first_pred = session.get('first_pred', 'no data found')
    first_proba = session.get('first_proba', 'no data found')   
    first_label = session.get('first_label', 'no data found')   
    second_pred = session.get('second_pred', 'no data found')
    second_proba = session.get('second_proba', 'no data found')   
    second_label = session.get('second_label', 'no data found') 
    print('session result:', session)
    session.clear()
    return jsonify({
        'first_pred': first_pred, 
        'first_label': first_label,
        'first_proba': first_proba,
        'second_pred': second_pred, 
        'second_label': second_label,
        'second_proba': second_proba
        })


@app.route('/predict', methods=['POST'])
@cross_origin(origin='http://localhost:5173')
def input_predict_text():
    #path to the classification model
    # classifier = TextClassifier.load_from_file('models/best-model.pt')
    model = mlflow.sklearn.load_model('models/LLM_deberta_v3_small')
    # model = mlflow.pytorch.load_model("../models/distilbert_finetuned_1/pytorch_model")
    #get input
    txt = request.get_json()['txt']
    encoded_txt = tokenizer(txt, return_tensors='pt')
    probabilities = predict(model, encoded_txt)
    first_pred, first_proba = get_first_prediction(probabilities)
    second_pred, second_proba = get_second_prediction(probabilities)
    first_label = get_label(first_pred)
    second_label = get_label(second_pred)
    session['first_pred'] = first_pred
    session['first_proba'] = first_proba
    session['first_label'] = first_label
    session['second_pred'] = second_pred
    session['second_proba'] = second_proba
    session['second_label'] = second_label
    session.permanent = True
    session.modified = True  # Force session save
    print('first:', first_pred, first_label, first_proba )
    print('second:', second_pred, second_label, second_proba)
    return jsonify({
        'first_pred': first_pred, 
        'first_label': first_label,
        'first_proba': first_proba,
        'second_pred': second_pred, 
        'second_label': second_label,
        'second_proba': second_proba
        })

if __name__ == "__main__":
    app.run(debug=True)

