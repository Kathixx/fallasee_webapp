from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import mlflow.sklearn
from flask import session
from datetime import timedelta

# MARENS Import
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
# END Marens Import

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




# Methods from deberta_v3.ipynb
# maybe only import methods?
# pipeline for predicting single sentences?
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
                key: val[i:i+batch_size].to(device) 
                for key, val in encodings.items()
            }
            outputs = model(**batch)
            probs = torch.softmax(outputs.logits, dim=-1).cpu().numpy()
            probabilities.extend(probs)
            
        # Clear GPU memory after each batch
        torch.mps.empty_cache()
    
    return np.array(probabilities)

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
    data_result = session.get('result', 'no data found')
    print('session result:', session)
    # session.clear()
    return jsonify({'prediction': data_result})

@app.route('/predict', methods=['POST'])
@cross_origin(origin='http://localhost:5173')
def input_predict_text():
    #get input
    fallacy = request.get_json()['fa']
    result = 'Fallacy' + fallacy 
    session['result'] = result
    session.permanent = True
    session.modified = True  # Force session save
    print('result:', result)
    print ('Session set: ', session.get('result'))
    return jsonify(result)


# @app.route('/predict', methods=['GET'])
# @cross_origin(origin='http://localhost:5173')
# def get_result():
#     result = []
#     data_result = session['my_result']
#     result.append ({'probs': data_result})
#     session.clear()
#     return jsonify(result)

# @app.route('/predict', methods=['POST'])
# @cross_origin(origin='http://localhost:5173')
# def input_predict_text():
#     #path to the classification model
#     # classifier = TextClassifier.load_from_file('models/best-model.pt')
#     model = mlflow.sklearn.load_model('models/LLM_deberta_v3_small')
#     #get input
#     fallacy = request.get_json()['fa']
#     # tokenize sentence
#     tokenized_fallacy = tokenize(fallacy)
#     base_probs = predict(model, tokenized_fallacy, batch_size=2)
#     predicted_labels = np.argmax(base_probs, axis=1)
#     predicted_label_probs = base_probs[np.arange(len(predicted_labels)), predicted_labels]
#     # result = {'title' : text, 'tag' : label.value}
#     session['my_result'] = predicted_label_probs
#     return jsonify({'result': predicted_label_probs})

if __name__ == "__main__":
    app.run(debug=True)

