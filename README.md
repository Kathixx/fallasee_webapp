# Capstone Project
**Authors:**
@Maren Borman, @Aylin Hanne, @Parya Tavaloki-Tehrani, @Katharina Baumgartner

## About the idea


## Used Datasets
We merged our dataset from different datasets, you can found here:
- [Argotario](https://github.com/UKPLab/argotario/tree/master)



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
