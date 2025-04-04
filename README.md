# Capstone Project
**Authors:**
@Maren Borman, @Aylin Hanne, @Parya Tavaloki-Tehrani, @Katharina Baumgartner

## About the Project
This project began as part of our Capstone Phase at [neuefische GmbH](https://www.neuefische.de). Our idea was to train an NLP Model to detect logical fallacies in sentences and build a web application where users can enter their own sentences.


## Used Datasets
We have merged our dataset from the following datasets:
1) [Jin et al. (2022)](https://arxiv.org/pdf/2202.13758). Dataset:
[LogicClimate](https://github.com/causalNLP/logical-fallacy/tree/main/data) 

2) Midhun Kandan. *Logical Fallacy Classification*. 2004. Dataset: [Hugging Face Dataset](https://huggingface.co/datasets/MidhunKanadan/logical-fallacy-classification)

3) [Yeh et al. (2024)](https://arxiv.org/pdf/2410.03457v1). Dataset:
[CoCoLoFa](https://github.com/Crowd-AI-Lab/cocolofa) 

4) [Chaves et al. (2025)](https://hal.science/hal-04834405/document). Dataset:
[FALCON](https://github.com/m-chaves/falcon-fallacy-classification) 

5) [Alhindi et al. (2022)](https://aclanthology.org/2022.emnlp-main.560.pdf). Dataset:
[Datasets](https://github.com/Tariq60/fallacy-detection) 

6) [Helwe et al. (2024)](https://arxiv.org/pdf/2311.09761). Dataset:
[MAFALDA](https://github.com/ChadiHelwe/MAFALDA) 

7) [Goffredo et al. (2023)](https://aclanthology.org/2023.emnlp-main.684.pdf). Dataset:
[ElecDeb60to20](https://github.com/pierpaologoffredo/ElecDeb60to20) 


## Categories of Logical Fallacies
After cleaning the data, we trained our model on the five most common fallacies present in the dataset, as well as on sentences that do not contain any logical fallacies.

Categories used for training:

| Category  |  Definition |
|---|---|
| Ad Hominem  |  This fallacy occurs when the speaker is attacking the other person or some aspect of them rather than addressing the argument itself. |
|Appeal to Authority | This fallacy occurs when an argument relies on the opinion or endorsement of an authority figure who may not have relevant expertise or whose expertise is questionable.| 
| Appeal to Emotion | This fallacy occurs when an emotion is used to support an argument, such as pity, fear, anger, etc..  |
| Faulty Generalization  | This fallacy occurs when an argument assumes something is true for a large population without having a large enough sample. A kind of overgeneralization. | 
| False Dilemma | This fallacy occurs when only two options are presented in an argument, even though more options may exist. A case of “either this or that.|
|None | There are no fallacies in the text.|

<br>

*Please note*: The definitions of the fallacies were taken from the research papers cited above or adjusted by us as needed.


## NLP Model

## Model Experiment Tracker

| # | Model Variant         | Class Weights | Epochs | LR     | Macro F1 | Test Accuracy | Notes                        |
|---|------------------------|---------------|--------|--------|----------|----------------|------------------------------|
| 1 | `distilbert-base`      | ❌ No          | 3      | 3e-5   | 0.65     | 0.74           |                     |
| 2 | `distilbert-base`      | ✅ Yes         | 4      | 5e-5   | 0.63     | 0.70           | Weighted loss + tuning       |
| 3 | `roberta-base`         | ✅ Yes (?)         | 3      | TBD   | TBD      | TBD            | To be trained                |
| 4 | `q3fer-fallacy-model`  | ❌ No          | 3      | 3e-5      | 0.68      | 0.74            | Pretrained on similar task   |
| 5 | ... | ...         | -      | -      | TBD      | TBD            | ...  |


## Web Application

...

## Run

### Backend
_in your backend folder, in different terminal tabs_

**1. Flask App:**
```bash
source .venv/bin/activate
python app.py # should run on http://127.0.0.1:5000
```

**2. MLFlow:**
```bash
source .venv/bin/activate
mlflow ui --port 5001 #should run on http://127.0.0.1:5001
```

to train the model and keep tracking with MLFlow, open another terminal tab:
```bash
source .venv/bin/activate
python -m modeling.train
```


<!-- In order to test that predict works on a test set you created run:

```bash
python modeling/predict.py models/linear data/X_test.csv data/y_test.csv
``` -->

**3. Ruff:** _(optional)_
```bash
source .venv/bin/activate
ruff check --watch
```

**more helpful commands from ruff:**
- `ruff rule F821`: more detailed explanation about the error message
- `ruff check --fix`: fix all errors, whith a fix-flag [*]
- `ruff format`: format the files

### Frontend
_in your frontend folder, in a new terminal tab_

**1. VueApp**
```bash
npm run dev # app should run on http://localhost:5173/
```




## Initial Setup

### Backend
_in the backend folder_


**1. Virtuell Environment, Install requirements**

```BASH
pyenv local 3.11.3
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements_dev.txt
```

The `requirements.txt` file contains the libraries needed for deployment.. of model or dashboard .. thus no jupyter or other libs used during development.

**2. MLFlow**

create a `mlflow_uri` file in the backend folder

```BASH
echo http://127.0.0.1:5001/ > .mlflow_uri
```

Handle errors:

```bash
# MLFlow server already running
pkill -f gunicorn
```

### Frontend
_everything will be installed globally, it's not importend in which folder you're right now_

**1. Node & NPM**: check if you have already node and npm installed

```bash
node -v # v23.7.0
npm -v # 11.2.0

# update if necessary
npm install -g npm@11.2.0
```
**2. VueCLI & Vite**
```bash
npm install -g @vue/cli
npm install vite
```

**3. Axios**
```bash
npm install axios
```