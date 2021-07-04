import yaml
import joblib
import numpy as np

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


def form_response(request):
    data = request.values()
    data = [list(map(int, data))]
    return predict(data)

def api_response(request):
    data = np.array([list(request.values())])
    response = predict(data)
    return { "response" : response }
