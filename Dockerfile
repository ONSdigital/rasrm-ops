FROM python:3.6-slim

ENV APP_SETTINGS=DockerConfig

WORKDIR /app
COPY . /app
EXPOSE 8003
RUN apt-get update -y && apt-get install -y python-pip && apt-get install -y curl
RUN pip3 install pipenv && pipenv install --deploy --system

ENTRYPOINT ["python3"]
CMD ["run.py"]
