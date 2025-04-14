from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask import session
from datetime import timedelta

import numpy as np
import torch
import mlflow.pytorch

from modeling.basic_functions import (
    tokenize,
)


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


def get_tokenized_text(txt):
    x_tokenized = tokenize(txt, "distilbert-base-uncased")
    return x_tokenized

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
    # first_pred = session.get('first_pred', 'no data found')
    # first_proba = session.get('first_proba', 'no data found')   
    # first_label = session.get('first_label', 'no data found')   
    # second_pred = session.get('second_pred', 'no data found')
    # second_proba = session.get('second_proba', 'no data found')   
    # second_label = session.get('second_label', 'no data found') 
    ad_hominem = session.get('0_ad_hominem', 'no data found')
    authority = session.get('1_authority', 'no data found')
    emotion = session.get('2_emotion', 'no data found')
    dilemma = session.get('3_dilemma', 'no data found')
    slope = session.get('4_slope', 'no data found')
    none = session.get('5_none', 'no data found')
    session.clear()
    return jsonify({
        '0_ad_hominem': ad_hominem,
        '1_authority': authority,
        '2_emotion': emotion,
        '3_dilemma': dilemma,
        '4_slope': slope,
        '5_none': none
        # 'first_pred': first_pred, 
        # 'first_label': first_label,
        # 'first_proba': first_proba,
        # 'second_pred': second_pred, 
        # 'second_label': second_label,
        # 'second_proba': second_proba
        })


@app.route('/predict', methods=['POST'])
@cross_origin(origin='http://localhost:5173')
def input_predict_text():
    model = mlflow.pytorch.load_model('./models/distilbert_multiclass_with_none/pytorch_model')
    #get input
    txt = request.get_json()['txt']
    tokenized_txt = get_tokenized_text(txt)
    # encoded_txt = tokenizer(txt, return_tensors='pt')
    probabilities = predict(model, tokenized_txt)
    print('All probabilites:', probabilities)
    # first_pred, first_proba = get_first_prediction(probabilities)
    # second_pred, second_proba = get_second_prediction(probabilities)
    # first_label = get_label(first_pred)
    # second_label = get_label(second_pred)
    # session['first_pred'] = first_pred
    # session['first_proba'] = first_proba
    # session['first_label'] = first_label
    # session['second_pred'] = second_pred
    # session['second_proba'] = second_proba
    # session['second_label'] = second_label
    session['0_ad_hominem'] = float(probabilities[0][0])
    session['1_authority'] = float(probabilities[0][1])
    session['2_emotion'] = float(probabilities[0][2])
    session['3_dilemma'] = float(probabilities[0][3])
    session['4_slope'] = float(probabilities[0][4])
    session['5_none'] = float(probabilities[0][5])
    session.permanent = True
    session.modified = True  # Force session save
    # print('second:', second_pred, second_label, second_proba)
    return jsonify({
        '0_ad_hominem': float(probabilities[0][0]),
        '1_authority': float(probabilities[0][1]),
        '2_emotion': float(probabilities[0][2]),
        '3_dilemma': float(probabilities[0][3]),
        '4_slope': float(probabilities[0][4]),
        '5_none': float(probabilities[0][5])
        # 'first_pred': first_pred, 
        # 'first_label': first_label,
        # 'first_proba': first_proba,
        # 'second_pred': second_pred, 
        # 'second_label': second_label,
        # 'second_proba': second_proba
        })

if __name__ == "__main__":
    app.run(debug=True)

