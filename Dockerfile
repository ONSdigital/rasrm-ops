FROM python:3.6

WORKDIR /app
COPY . /app
EXPOSE 8003
RUN pip3 install pipenv && pipenv install --deploy --system

ENTRYPOINT ["python3"]
CMD ["run.py"]
