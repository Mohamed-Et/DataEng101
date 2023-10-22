# Commands to run : 
# 1-> docker build -t name:version . 
# 2-> docker run -it name:version param1 param2...
# -it for interacive
# . for specifying the Dockerfile exists in the current directory

FROM python:3.12.0

RUN pip install pandas sqlalchemy psycopg2 requests

WORKDIR /app

COPY dirtypipeline.py dirtypipeline.py

ENTRYPOINT [ "python", "dirtypipeline.py" ]