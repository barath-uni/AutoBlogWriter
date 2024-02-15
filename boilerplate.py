
# Python 3

# Create a boiler plate file for using a hugging-face model in a flask server

import os
import sys
import json
import logging
import argparse
import requests
import numpy as np
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from flask import Flask, request, jsonify

app = Flask(__name__)

MODEL = None
DEVICE = "cpu"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        input = request.form['input']
        output = input
        return render_template('index.html', output=output)

# Load the model
def load_model(model_name_or_path):
    global MODEL
    global DEVICE

    # If a model path is specified, load the model
    if model_name_or_path:
        tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
        MODEL = AutoModelForSequenceClassification.from_pretrained(model_name_or_path)
        MODEL.to(DEVICE)
        MODEL.eval()
        print(f"Loaded model {model_name_or_path}")
    else:
        raise Exception("You must specify a model path")

# Predict using the model
def predict(sentence):
    global MODEL
    global DEVICE

    tokenized_sentence = tokenizer.encode(sentence, add_special_tokens=True)
    input_ids = torch.tensor([tokenized_sentence]).to(DEVICE)
    with torch.no_grad():
        output = MODEL(input_ids)
        prediction = torch.argmax(output[0]).item()
    return prediction

# Route for the API
@app.route("/predict", methods=["POST"])
def predict_sentiment():
    if MODEL is None:
        return jsonify({"error": "Model not loaded"}), 500

    data = request.get_json()
    if "sentence" not in data.keys():
        return jsonify({"error": "Input not found"}), 400

    sentence = data["sentence"]
    prediction = predict(sentence)
    return jsonify({"prediction": prediction})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", type=str, default="", help="Path to the model")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host for the server")
    parser.add_argument("--port", type=int, default=5000, help="Port for the server")
    args = parser.parse_args()

    load_model(args.model_path)

    app.run(host=args.host, port=args.port)