from get_data import read_params
import argparse
import mlflow
from mlflow.tracking import MlflowClient
from pprint import pprint
import joblib
import os
import mlflow.pyfunc


def log_production_model(config_path):
    config = read_params(config_path)

    mlflow_config = config["mlflow_config"]
    model_name = mlflow_config["registered_model_name"]
    remote_server_uri = mlflow_config["remote_server_uri"]
    model_dir = config["model_dir"]

    mlflow.set_tracking_uri(remote_server_uri)

    # our exp id  is 1 under artifacts folder
    runs = mlflow.search_runs(experiment_ids=1)

    highest_silhouette_score = runs["metrics.silhouette_score"].sort_values(
        ascending=False).reset_index().iloc[0, 1]

    highest_run_id = runs[runs["metrics.silhouette_score"]
                          == highest_silhouette_score].iloc[0].run_id

    client = MlflowClient()
    for mv in client.search_model_versions(f"name='{model_name}'"):
        mv = dict(mv)

        if mv["run_id"] == highest_run_id:
            current_version = mv["version"]
            logged_model = mv["source"]
            #pprint(mv, indent=4)
            client.transition_model_version_stage(
                name=model_name,
                version=current_version,
                stage="Production"
            )
        else:
            current_version = mv["version"]
            pprint(mv, indent=4)
            client.transition_model_version_stage(
                name=model_name,
                version=current_version,
                stage="Staging"
            )

    loaded_model = mlflow.pyfunc.load_model(logged_model)
    model_path = config["webapp_final_model_dir"]

    joblib.dump(loaded_model, model_path)
    joblib.dump(loaded_model, model_dir)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    data = log_production_model(parsed_args.config)
