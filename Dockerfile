FROM continuumio/anaconda3
LABEL maintainer = "github@asok-mirror"

## App Configuration
COPY . /usr/app/
WORKDIR /usr/app/
RUN pip install -r requirements.txt
CMD python app.py