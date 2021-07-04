import yaml
import joblib

params_path = "params.yaml"

def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


def predict(data):
    config = read_params(params_path)
    model_dir = config["webapp_final_model_dir"]
    model = joblib.load(model_dir)
    prediction = model.predict(data).tolist()[0]
    return prediction

def form_response(dict_request):
    data = dict_request.values()
    return data