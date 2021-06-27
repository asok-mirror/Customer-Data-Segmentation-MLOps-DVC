#data pre-processing step
#save it in data\processed folder

import os
import argparse
import pandas as pd
from get_data import read_params

def process_and_save_data(config_path):
    config = read_params(config_path)
    raw_data_path = config["load_data"]["raw_dataset_csv"]
    processed_data_path = config["process_data"]
    df = pd.read_csv(raw_data_path)
    #In the EDA, we found there is no null values so skipping 
    #and saving the file to processed folder
    print(df.isna().sum()) #no null values
    df.to_csv(processed_data_path, index=False)

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    process_and_save_data(parsed_args.config)
