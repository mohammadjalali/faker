FROM python:3.11-slim-buster

WORKDIR /producer/

COPY producer.py requirements.txt /producer/

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "producer.py" ]
