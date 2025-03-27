from logging import getLogger
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
import random 
import pickle
import warnings
import mlflow
from mlflow.sklearn import save_model  # , log_model

# import the functions, which we have defined in the feature_engineering.py script
from modeling.feature_engineering import (
    drop_column,
    # function_name
)

# import the functions, which we have defined in the train.py script
from modeling.train import (
    __get_data,
    __compute_and_log_metrics,
)

from modeling.config import TRACKING_URI, EXPERIMENT_NAME

warnings.filterwarnings("ignore")
logger = getLogger(__name__)

def run_training():
    logger.info(f"Getting the data")
    y_test = pd.read_csv("../data/y_test.csv")
    y_train = pd.read_csv("../data/y_train.csv")

    logger.info("Training baseline model and tracking with MLFlow")
    mlflow.set_tracking_uri(TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)

    logger.info("Running the baseline model")
    with mlflow.start_run():
        # predict y randomly 
        y_train_list = y_train.tolist()
        y_train_pred = random.choices(y_train_list, k=len(y_train))
        y_test_pred = random.choices(y_train_list, k=len(y_test))

        # in mlFlow a tag has a name (like 'modelX') and a corresponding value (here: true).
        mlflow.set_tag("mlflow.runName", "run_name")
        mlflow.set_tag("baseline_model", "True")

        logger.info("Evaluating the baseline model")
        __compute_and_log_metrics(y_train, y_train_pred, "train")
        __compute_and_log_metrics(y_test, y_test_pred, "test")

        logger.info("this is obviously fishy")

        # saving the model
        # logger.info("Saving model in the model folder")
        # path = "models/linear"
        # save_model(sk_model=reg, path=path)

if __name__ == "__main__":
    import logging

    logger = logging.getLogger()
    logging.basicConfig(format="%(asctime)s: %(message)s")
    logging.getLogger("pyhive").setLevel(logging.CRITICAL)  # avoid excessive logs
    logger.setLevel(logging.INFO)

    run_training()