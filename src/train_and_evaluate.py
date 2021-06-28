#Load the train and test files
#train model
#save the metrics and params

import os
import warnings
import sys
import pandas as pd
import numpy as np
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import hdbscan
import argparse
from get_data import read_params
import argparse
import joblib
import json

def eval_metrics(data, hdbscan_labels):
    silhouette = silhouette_score(data, hdbscan_labels)
    no_of_clusters = len(set(hdbscan_labels)) - (1 if -1 in hdbscan_labels else 0)
    return silhouette, no_of_clusters


def train_and_evaluate(config_path):
    config = read_params(config_path)
    processed_data_path = config["process_data"]
    random_state = config["base"]["random_state"]
    model_dir = config["model_dir"]

    min_cluster_size = config["estimators"]["HHDBSCAN"]["params"]["min_cluster_size"]
    min_samples = config["estimators"]["HHDBSCAN"]["params"]["min_samples"]
    cluster_selection_epsilon = config["estimators"]["HHDBSCAN"]["params"]["cluster_selection_epsilon"]

    data = pd.read_csv(processed_data_path)

    data = data.drop(columns= ['DATE', 'SP500'], axis = 1)

    pipeline = Pipeline([
                    ('scaler', StandardScaler()),
                    ('estimator', hdbscan.HDBSCAN(
                        min_cluster_size=min_cluster_size, 
                        min_samples=min_samples, 
                        cluster_selection_epsilon = cluster_selection_epsilon
                        ))              
                ])


    pipeline.fit(data)
    estimator = pipeline.named_steps['estimator']

    silhouette_score, no_of_clusters = eval_metrics(data, estimator.labels_)

    print('The silhouette score is: %f' % silhouette_score)
    print('The number of cluster is: %d' % no_of_clusters)

################################################################
    scores_file = config["reports"]["scores"]
    params_file = config["reports"]["params"]

    with open(scores_file, "w") as f:
        scores = {
            "silhouette_score": silhouette_score,
            "no_of_clusters": no_of_clusters
        }
        json.dump(scores, f, indent=4)

    with open(params_file, "w") as f:
        params = {
            "min_cluster_size": min_cluster_size,
            "min_samples": min_samples,
            "cluster_selection_epsilon": cluster_selection_epsilon
        }
        json.dump(params, f, indent=4)
################################################################

    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "model.joblib")

    joblib.dump(pipeline, model_path)

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    train_and_evaluate(parsed_args.config)