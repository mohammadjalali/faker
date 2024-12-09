FROM python:3.11-slim-buster

WORKDIR /consumer/

COPY consumer.py requirements.txt /consumer/

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "consumer.py" ]
