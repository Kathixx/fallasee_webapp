# Research improving Distilbert performance

## Model setup

**Article BERT:**
https://arxiv.org/pdf/1810.04805

- BERT:
    - Bidirectional Encoder Representations from Transformers
- BERT uses "masked language model" (MLM) pre-training objective:
    - MLM randomly masks some of tokens from the input 


**Article DistilBert:**
https://arxiv.org/pdf/1910.01108

DistilBERT authors sowed that it is possible to reduce BERT by 40%, while retaining 97% of its language understanding capabilities and being 60% faster.

Difference between DistilBERT and BERT:
- same general arcitechture
- token-type embeddings and pooler are removed, while number of layers is reduced by factor 2 in DistilBERT
- BERT has 6 layers

**Architechture DistilBert:**

- 6 Transformer layers
- Each layer has 12 attention heads that focus on different part of the input text to understand context
- 768-dimenional hidden states: 
    - hidden states are the internal representations of tokens (words or subwords) as they pass through the layers
    - each token in the input sequence is converted into a 768-dimensional vector at every layer
    - vector contains numerical values that encode information about the token's meaning and its relationship to other tokens
- 67 million parameters

Key Components:
- Tokenization:
    - text is split into smaller units called tokens using WordPiece tokenizer (e.g. "unhappiness" becomes ["un", "##happiness"])
    - tokens are converted into numerical IDs that the model can process

- Embeddings:
    - Token embeddings: maps tokens to vectors, that represents its meaning
    - Positional embeddings: Encodes order of words in sentence
    - **No segment embeddings:** DistilBERT omits BERT’s next-sentence prediction capability.

- The text passes through 6 **Transformer layers**, where each layer performs:
    1. Multi-head self-attention:
        - 12 parallel attention heads
        - weights relationships between words
    2. Feed-forward network:
        - Processes these relationships further using GELU activation functions.
    3. Layer normalization & residual connections:
        - Stabilizes training and helps retain information across layers.

## How to improve the F1 macro

### Model architechture and training adjustments 

**Hyperparameter Tuning:**
- use lower learning rate (e.g. 2e-5)
- use smaller batch size
- train for more epochs (with early stopping to prevent overfitting)
- use weighted or macro F1 loss instead of cross-entropy

Adjust Config:
https://huggingface.co/distilbert/distilbert-base-uncased/blob/main/config.json

Adjust Trainer:
https://huggingface.co/docs/transformers/v4.51.1/en/main_classes/trainer#transformers.TrainingArguments


**Structural Features:**
- incorporate logical structure trees or argument relations as input features

### Reduce overfitting

Regularization techniques:
- Increase dropout: Add dropout layers (e.g., nn.Dropout(0.3-0.5)) before the classifier head or between transformer layers.
- Weight decay: Add L2 regularization (e.g., weight_decay=0.01 in your optimizer).
- Layer-wise learning rate decay: Use lower learning rates for earlier transformer layers (e.g., 2e-5 for layer 6, 1.8e-5 for layer 5, etc.).

### Advanced techniques

**Model ensembling:**
- combine prediction of multiple DistilBERT fine-tuned models

### Evaluation

**Error analysis:**
- identify classes with poor performance and refine their traiing data
- look at sentences if there is a pattern
