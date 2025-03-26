from logging import getLogger
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
import pickle
import warnings
import mlflow
from mlflow.sklearn import save_model  # , log_model

# import the functions, which we have defined in the feature_engineering.py script
from modeling.feature_engineering import (
    drop_column,
    # function_name
)

from modeling.config import TRACKING_URI, EXPERIMENT_NAME

warnings.filterwarnings("ignore")
logger = getLogger(__name__)


def __get_data():
    logger.info("Getting the data")
    # load the data
    df = pd.read_csv("data/path.csv")

    # define target and features
    Y = df["target"]
    X = df.drop(["target"])

    # splitting into train and test
    X_train, X_test, y_train, y_test = train_test_split(
        X, Y, test_size=0.30, random_state=42
    )

    ## in order to exemplify how the predict will work.. we will save the y_train
    logger.info("Saving test data in the data folder")
    X_test.to_csv("data/X_test.csv", index=False)
    y_test.to_csv("data/y_test.csv", index=False)

    logger.info("Feature engineering on train")
    X_train = drop_column(X_train, col_name="Unnamed: 0")
    X_train = drop_column(X_train, col_name="Quakers")

    # feature eng on test data
    logger.info("Feature engineering on test")
    X_test = drop_column(X_test, col_name="Unnamed: 0")
    X_test = drop_column(X_test, col_name="Quakers")

    return X_train, X_test, y_train, y_test


def __compute_and_log_metrics(
    y_true: pd.Series, y_pred: pd.Series, prefix: str = "train"
):
    mse = mean_squared_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)

    logger.info(
        "Linear Regression performance on "
        + str(prefix)
        + " set: MSE = {:.1f}, R2 = {:.1%},".format(mse, r2)
    )
    mlflow.log_metric(prefix + "-" + "MSE", mse)
    mlflow.log_metric(prefix + "-" + "R2", r2)

    return mse, r2


def run_training():
    logger.info(f"Getting the data")
    X_train, X_test, y_train, y_test = __get_data()

    logger.info("Training simple model and tracking with MLFlow")
    mlflow.set_tracking_uri(TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)

    # model
    logger.info("Training the model")
    with mlflow.start_run():
        # define model
        reg = LinearRegression().fit(X_train, y_train)

        # taking some parameters out of the feature eng.. in your case you can use the params from CV
        params = {
            "altitude_low_meters_mean": 11,
            "altitude_high_meters_mean": 22,
            "altitude_mean_log_mean": 33,
            "fit_intercept": True,
        }

        mlflow.log_params(params)
        # in mlFlow a tag has a name (like 'modelX') and a corresponding value (here: true).
        mlflow.set_tag("mlflow.runName", "run_name")
        mlflow.set_tag("modelX", "True")

        y_train_pred = reg.predict(X_train)
        __compute_and_log_metrics(y_train, y_train_pred)

        y_test_pred = reg.predict(X_test)
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
