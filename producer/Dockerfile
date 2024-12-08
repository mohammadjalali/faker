FROM python:3.11-slim-buster

WORKDIR /producer/

COPY producer.py requirements.txt /producer/

RUN pip install -r requirements.txt

CMD [ "python", "producer.py" ]
