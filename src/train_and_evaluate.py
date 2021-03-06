# Load the train and test files
# train model
# save the metrics and params

import os
import warnings
import sys
import pandas as pd
import numpy as np
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
from urllib.parse import urlparse
import argparse
from get_data import read_params
import argparse
import joblib
import json
import mlflow
import mlflow.sklearn


def eval_metrics(data, kmeans_labels):
    silhouette = silhouette_score(data, kmeans_labels)
    return silhouette


def train_and_evaluate(config_path):
    config = read_params(config_path)
    processed_data_path = config["process_data"]
    random_state = config["base"]["random_state"]
    #model_dir = config["model_dir"]
    #webapp_final_model_dir = config["webapp_final_model_dir"]
    trained_data = config["trained_data"]
    mlflow_config = config["mlflow_config"]
    remote_server_uri = mlflow_config["remote_server_uri"]

    n_clusters = config["estimators"]["KMeans"]["params"]["n_clusters"]

    data = pd.read_csv(processed_data_path)

    data = data.drop(columns=['CustomerID'], axis=1, errors='ignore')

    data['Gender'] = data.Gender.map({'Male': 1, 'Female': 2})

    print(data.head())

####################### MLFLOW #######################

    mlflow.set_tracking_uri(remote_server_uri)

    mlflow.set_experiment(mlflow_config["experiment_name"])

    with mlflow.start_run(run_name=mlflow_config["run_name"]) as mlops_run:

        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('estimator', KMeans(n_clusters=n_clusters, random_state=random_state))
        ])

        pipeline.fit(data)
        estimator = pipeline.named_steps['estimator']

        silhouette_score = eval_metrics(data, estimator.labels_)

        #print('The silhouette score is: %f' % silhouette_score)
        mlflow.log_param("n_clusters", n_clusters)
        mlflow.log_metric("silhouette_score", silhouette_score)

        tracking_url_type_store = urlparse(mlflow.get_artifact_uri()).scheme

        if tracking_url_type_store != "file":
            mlflow.sklearn.log_model(
                pipeline,
                "model",
                registered_model_name=mlflow_config["registered_model_name"])
        else:
            mlflow.sklearn.load_model(pipeline, "model")

        labels = pd.DataFrame(estimator.labels_)
        data_with_labels = pd.concat((data, labels), axis=1)
        data_with_labels = data_with_labels.rename({0: 'labels'}, axis=1)

        data_with_labels.to_csv(trained_data, index=False)

    ################################################################
        # scores_file = config["reports"]["scores"]
        # params_file = config["reports"]["params"]

        # with open(scores_file, "w") as f:
        #     scores = {
        #         "silhouette_score": silhouette_score
        #     }
        #     json.dump(scores, f, indent=4)

        # with open(params_file, "w") as f:
        #     params = {
        #         "cluster_size": n_clusters,
        #     }
        #     json.dump(params, f, indent=4)
    ################################################################

        # os.makedirs(model_dir, exist_ok=True)
        # os.makedirs(webapp_final_model_dir, exist_ok=True)

        # model_path = os.path.join(model_dir, "model.joblib")
        # webapp_final_model_dir = os.path.join(
        #     webapp_final_model_dir, "model.joblib")

        # joblib.dump(pipeline, model_path)
        # # Save the model to prediction service
        # joblib.dump(pipeline, webapp_final_model_dir)

####################### END OF MLFLOW #######################

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    train_and_evaluate(parsed_args.config)
