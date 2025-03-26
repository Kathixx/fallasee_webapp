# Capstone Project
**Authors:**
@Maren Borman, @Aylin Hanne, @Parya Tavaloki-Tehrani, @Katharina Baumgartner

## About the idea




## Requirements:
- pyenv with Python: 3.11.3

### Setup
Use the requirements file in this repo to create a new environment.

```BASH
pyenv local 3.11.3
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements_dev.txt
```

The `requirements.txt` file contains the libraries needed for deployment.. of model or dashboard .. thus no jupyter or other libs used during development.

### MLFlow
create a `mlflow_uri` file:

```BASH
echo http://127.0.0.1:5000/ > .mlflow_uri
```

**Creating an MLFlow experiment**

Create a new experiment and save the  name in the [config file](modeling/config.py).
```bash
mlflow experiments create --experiment-name 0-template-ds-modeling
```


**Handle errors:** 

```bash
# MLFlow server already running
pkill -f gunicorn
```


## Usage

### Run the backend and MLFlow
in the terminal in your backend folder

```bash
source .venv/bin/activated

mlflow ui
```

MLFlow is running on: [http://127.0.0.1:5000](http://127.0.0.1:5000)


### Train/Test the model
in a new terminal in your backend folder (MLFlow is still running!)

```bash
#activate env
source .venv/bin/activate

python -m modeling.train
```

<!-- In order to test that predict works on a test set you created run:

```bash
python modeling/predict.py models/linear data/X_test.csv data/y_test.csv
``` -->
