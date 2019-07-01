FROM tiangolo/uvicorn-gunicorn:python3.7

LABEL maintainer="Kevin Hill <kah.kevin.hill@gmail.com>"



COPY ./app /app
WORKDIR /app
RUN pip install fastapi
RUN pip install -r requirements.txt