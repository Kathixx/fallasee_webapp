import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.class_weight import compute_class_weight
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer, Pipeline 
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score, classification_report, confusion_matrix
import mlflow
from mlflow.transformers import log_model
import logging 
import torch
from torch.nn import CrossEntropyLoss
from mlflow.models.signature import infer_signature



from sklearn.model_selection import train_test_split
import pickle
import warnings
warnings.filterwarnings('ignore') 
from mlflow.sklearn import save_model 
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"  # This tells Hugging Face: “Don’t use parallel tokenization — avoid possible deadlocks.”

import seaborn as sns
import matplotlib.pyplot as plt

import config 

MODEL_NAME = "distilbert-base-uncased" # pulls the general-purpose DistilBERT model
DATA_PATH = "../data/data_small.csv"
TRACKING_URI = config.TRACKING_URI #??? TRACKING_URI = open("../.mlflow_uri").read().strip()
EXPERIMENT_NAME = config.EXPERIMENT_NAME

logging.basicConfig(format="%(asctime)s: %(message)s") # Configure logging format to show timestamp before every message

logger = logging.getLogger()
logger.setLevel(logging.INFO) # Only show logs that are INFO or more important (e.g., WARNING, ERROR) — but ignore DEBUG.

# Load and preprocess data
logger.info("Loading and preprocessing data...")
df = pd.read_csv(DATA_PATH)

# use only 10 rows to test end-to-end run (comment this line out later)
df = df.sample(10, random_state=42).reset_index(drop=True)

le = LabelEncoder()
df["label"] = le.fit_transform(df["logical_fallacies"])
dataset = Dataset.from_pandas(df[["text", "label"]])
dataset = dataset.train_test_split(test_size=0.3)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def tokenize(batch):
    return tokenizer(batch["text"], padding=True, truncation=True)

dataset = dataset.map(tokenize, batched=True)

# Initialize model, we should use AutoModelForSequenceClassification and not AutoModelForMaskedLM because we are doing classification
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=len(le.classes_))


# # Get labels from training set
# y_train = dataset["train"]["label"]
# # all_labels = list(range(len(le.classes_))) 
# present_labels = np.unique(y_train)

# # Compute class weights
# class_weights = compute_class_weight(class_weight='balanced', classes=present_labels, y=y_train)
# class_weights_tensor = torch.tensor(class_weights, dtype=torch.float)


# Get full list of label indices
full_class_indices = np.arange(len(le.classes_))  # e.g., [0, 1, 2, 3, 4, 5]

# Get only the classes that appear in y_train
y_train = dataset["train"]["label"]
present_classes = np.unique(y_train)

# Compute weights ONLY for the present ones
present_weights = compute_class_weight(
    class_weight="balanced",
    classes=present_classes,
    y=y_train
)

# Initialize full weight vector with 0s, then insert the computed ones
full_weights = np.zeros(len(full_class_indices), dtype=np.float32)
for idx, cls in enumerate(present_classes):
    full_weights[cls] = present_weights[idx]

# Convert to tensor
class_weights_tensor = torch.tensor(full_weights, dtype=torch.float)

# Hugging Face’s Trainer does not support class weights out-of-the-box, so we must override the loss

class WeightedTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False, **kwargs): # **kwargs captures unexpected/optional arguments (like num_items_in_batch) without breaking your function
        labels = inputs.get("labels")
        outputs = model(**inputs)
        logits = outputs.get("logits")

        loss_fn = torch.nn.CrossEntropyLoss(weight=class_weights_tensor.to(model.device))
        loss = loss_fn(logits, labels)

        return (loss, outputs) if return_outputs else loss
    
    # Define metric logging function
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = logits.argmax(axis=1)
    acc = accuracy_score(labels, preds)
    precision = precision_score(labels, preds, average="macro")
    recall = recall_score(labels, preds, average="macro")
    f1 = f1_score(labels, preds, average="macro")
    return {"accuracy": acc, "precision": precision, "recall": recall, "f1": f1}

# TrainingArguments This config tells the Trainer: 
# “Train for 3 epochs, evaluate and save the model after each one, 
# use moderate batch sizes, 
# and keep logs and checkpoints local — don’t auto-report to external dashboards.” --> can it be set to report to MLFlow?

args = TrainingArguments(
    output_dir="fallacy-model",
    learning_rate=3e-5, # added for fine-tuning, 5e-5 by default
    weight_decay=0.01,  # added for fine-tuning, 0 by default
    evaluation_strategy="epoch",
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    num_train_epochs=4,  # increased from 3 for fine-tuning
    logging_dir="./logs",
    save_strategy="epoch",
    report_to="none"
)

# Train using Trainer and log to MLflow
# setting the MLFlow connection and experiment

from transformers import pipeline
from mlflow.models.signature import infer_signature

# Define training params to log
params = {
      "learning_rate": 3e-5,
      "weight_decay": 0.01,
      "num_train_epochs": 4,
      "evaluation_strategy": "epoch",
  }


# setting the MLFlow connection and experiment
mlflow.set_tracking_uri(TRACKING_URI)
mlflow.set_experiment(EXPERIMENT_NAME)


with mlflow.start_run():
    run = mlflow.active_run()
    print("Active run_id: {}".format(run.info.run_id))

    mlflow.set_tag("model_name", MODEL_NAME)
    mlflow.log_params(params)

    trainer = WeightedTrainer(
        model=model,
        args=args,
        train_dataset=dataset["train"],
        eval_dataset=dataset["test"],
        tokenizer=tokenizer,
        compute_metrics=compute_metrics
    )

    trainer.train()
    trainer.evaluate()

    # Wrap model in a Hugging Face pipeline so MLflow can log it properly
    pipeline = pipeline("text-classification", model=trainer.model, tokenizer=tokenizer)
    
    # Define training params to log
    # Use a sample from the dataset because mlflow.log_model() still requires an example input and output (not the full dataset)
    sample_input = [dataset["test"][0]["text"]]  # must be wrapped in a list
    example_input = [sample_input]
    sample_output = pipeline(sample_input)
    signature = infer_signature(sample_input, sample_output)

    # Log model with input example and signature
    log_model(
        pipeline, 
        artifact_path="model", 
        input_example=example_input, 
        signature=signature
        ) 

# Even though with mlflow.start_run(): handles ending automatically, it's good style to include the end
mlflow.end_run()
