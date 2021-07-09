
# Customer Purchase Pattern Segmentation

Customer Segmentation is a KMeans based Clustering app based on the
 [MallCustomer Dataset](https://www.kaggle.com/vjchoudhary7/customer-segmentation-tutorial-in-python)


## Prerequisite
Download [Docker Desktop](https://www.docker.com/products/docker-desktop) 


## Project Structure is based on 
Project based on the [cookiecutter](https://drivendata.github.io/cookiecutter-data-science/) data science project template. 

## Usage
Build the docker at the root of the app 

```docker
docker-compose up --build
```

## Serving Ports
```ports
web server @ 0.0.0.0:5000

MLflow server @ 0.0.0:5001
```

## Running Experiments
add the data set to data_given\dataset

```
dvc add dataset.csv
````
change the model parameters in the params.yaml file 

to run ML pipelines

```
dvc repro
```

The experiments are captured in the local SQLite dB

## Other Helpful Commands
run MLflow tracking server without docker

```
mlflow server --backend-store-uri sqlite:///customerSegmentationmlflow.db --default-artifact-root .\artifacts -h 0.0.0.0 -p 5001
```

run web app
```
python app.py 
```

experient the code using jupyter lab
```
jupyter lab notebooks/
```

## References
Azure Container registry setup
```
https://docs.microsoft.com/en-us/azure/container-instances/tutorial-docker-compose
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)