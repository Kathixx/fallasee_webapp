# LLMs

1. Overview of LLMs
2. Which LLMs are there/can we use
3. How implement LLMs in Python (How RAG can help)

## **1. Overview of LLMs**

https://rpradeepmenon.medium.com/introduction-to-large-language-models-and-the-transformer-architecture-534408ed7e61

Large Language Models (LLMs) are trained on massive amounts of text data. As a result, they can generate coherent and fluent text. GPT (Generative Pre-trained Transformer) is an example of a LMM. 

The basic premise of a LMM is to predict the next word or sub-word (called tokens) based on observed text:

![image](https://miro.medium.com/v2/resize:fit:1256/format:webp/1*zlj8N1mdfX-OLfxDqrzmig.png)

**The Transformer Architecture**

The transformer architecture is the fundamental building block of all LLMs. A simplified version of the Transformer Architecture:

![image](https://miro.medium.com/v2/resize:fit:1278/format:webp/1*BIA2niZY7XpPlOsLKD2Qrw.png)

1. Inputs and Input Embeddings:
- tokens entered by the user
- need to be converted into numerical format called "input embeddings", represent words as numbers
- during training, model learns how to create these embeddings, so that similar vectors represent words with similar meanings
2. Positional Encoding:
- encode the position of each word in the input sequence as a set of numbers
- fed into Transformer model, along with input embeddings
3. Encoder: 
- part of neural network that processes the input text and generates a series of hidden states that capture the meaning and context of the text
- encoder first tokenizes the input text into sequence of tokens and then applies a series of self-attentio layers
- multiple layers of the encoder are used in the transformer
4. Outputs (shifted right):
- decoder learns how to guess the next word by looking at the words before it
- to do this, output sequence moved over one spot to the right; that way, the decoder can only use the previous words
5. Output embeddings:
- output must be changed to numerical format, known as "output embeddings"
- similar to input embeddings and go through positional encoding
- a loss function is used, which measures the difference between a models prediction and actual target values
- output embeddings are used during both training and inference in GPT
- during training, compute loss function and update parameters
- during inference, generate output text
6. Decoder:
- positionally encoded input and output embeddings go through decoder
- decoder is part of model that generates output sequence based on encoded input
- decoder generates natural language text based on input sequence and context learned by encoder
- multiple layers
7. Linear Layer and Softmax:
- linear layer maps output embeddings of decoder to higher-dimensional space
- transform output embeddings into the original input space
- softmax function for generating probability distribution of each output token

**Comparison to other models**

Transformer architecture beats out other ones like RNN and LSTMs for natural language processing. Outperformance because of **"attention mechanism"** concept -> Let's the model focus on different parts of input sequence when making output, attention to the context. Fastens up training time.

## **2. Which LLMs are there/can we use**

1. RoBERTa-Large
2. DeBERTa-v3
3. GPT-3.5/4 
4. Llama-2-13b
5. BERT-base 

## **3. How implement LLMs in Python**

***1. Environment Setup***

Install core packages:

```python
pip install transformers torch langchain chromadb llmclassifier
```

***2. Data Preparation***

Multi-Hot Encode for multi-label classification:
- when a text can belong to multiple fallacy classes simultaneously
- for this, each entry in the column should represent the labels of a single sample, so a list of labels inside the specific row ["label1", "label2"]

```python
mlb = MultiLabelBinarizer()
multi_hot_labels = mlb.fit_transform(fallacy_labels)
```

Tokenize the text:
```python
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("roberta-large") 
texts = ["text"]
labels = ["text"]
```

Logical structure trees:
- a method to enhance LLMs classification by explicitly mapping logical relationships between arguments and connective phrases
- identifies mismatches between logical connections
- recommended for complex multi-label tasks and domain-specificity
- source: https://aclanthology.org/2024.emnlp-main.730.pdf 

```python
def add_logical_structure(text): 
    return enhanced_text 
```

***3. Model Initialization***

```python
from llmclassifier import LLMTextClassifier
from transformers import AutoModelForSequenceClassification

# Option 1: Pre-built classifier
classifier = LLMTextClassifier(
    categories=["ad_hominem", "false_cause", ...],
    model_name="roberta-large"
)

# Option 2: Custom fine-tuning
model = AutoModelForSequenceClassification.from_pretrained(
    "microsoft/deberta-v3-large",
    num_labels=num_classes,
    problem_type="multi_label_classification"
)
```
***4. RAG Integration***

Retrieval_Augmented Generation (RAG) is a technique that combines **retrieval** (fetching relevant information from external knowledge base) with **generation** (using an LLM to process and classify or generate outputs). RAG can help to dynamically retrieving relevant information (e.g., fallacy definitions) to improve models understanding and accuracy.

1. Retrieve:
- Use a vector database or other retrieval mechanism to fetch relevant information based on the input text.

2. Augment:
- Combine the retrieved information with the input text to create a richer prompt for the LLM.

3. Generate:
- Pass the augmented input to the LLM for classification or prediction

```python
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

# Create vector store for fallacy definitions
vector_db = Chroma.from_texts(
    texts=["Ad hominem: Attacking the person...", ...],
    embedding=HuggingFaceEmbeddings()
)

def retrieve_fallacy_context(query):
    return vector_db.similarity_search(query, k=3)
```

***5. Training Pipeline***

1. Augment text (RAG):
- enrich training text with retrieved context (defintion or examples of logical fallacies) to help LLM understanding the task better

```python 
# Augment text with retrieved context
enhanced_texts = [
    f"{text} [CONTEXT]{retrieve_fallacy_context(text)}" 
    for text in texts
]
```
2. Fine-tuning training configuration

```python
training_args = TrainingArguments(
    output_dir="./results",                  # Directory to save checkpoints
    per_device_train_batch_size=8,           # Batch size per GPU/CPU
    num_train_epochs=3,                      # Number of training passes
    learning_rate=5e-5,                      # Step size for weight updates
)
```
3. Trainer Setup

```python
trainer = Trainer(
    model=model,                    # Your pre-trained LLM (e.g., DeBERTa, RoBERTa)
    args=training_args,             # Configuration from above
    train_dataset=tokenized_dataset # Augmented and tokenized data
)

trainer.train()
```

***6. Inference with Explanation***

```python
def classify_with_explanation(text):
    context = retrieve_fallacy_context(text)
    prompt = f"""
    Classify logical fallacies in: {text}
    Context: {context}
    Possible labels: {classifier.categories}
    """
    
    return classifier.predict(prompt)
```
