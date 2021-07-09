mlflow server --backend-store-uri sqlite:///customerSegmentationmlflow.db --default-artifact-root .\artifacts -h 127.0.0.1 -p 5001

docker build -t customer-segmentation .

#docker-compose up --build

https://docs.microsoft.com/en-us/azure/container-instances/tutorial-docker-compose