## FAKER the Maker

This is a simple application to stream fake data from kafka to elasticsearch.
The application is made of `producer`, `consumer`, `apache kafka`, and `elasticsearch`.

- The producer gets data from <https://fakerapi.it/api/v2/texts?_quantity=100&_locale=fa_IR>
  and puts to `Kafka`.

- The consumer reads data from `Kafka` and puts data to `Elasticsearch`.

- The api can tag the contents and filter the contents of `Elasticsearch`.
  You can see <http://localhost:8000/docs> to findout what apis you can use.

- The project is not completed. for completing the project the following steps need to get done.

- [ ] An API for tagging the elasticsearch contents.

- [ ] The kafka image in docker compose does not work properly and it is due to the kafka network configuration.

- For the above reason docker compose will not work, but for developing and testing, you can run a kafka image on port `9092`, and run the producer and consumer localy.
As a result, you can follow the following steps to run the project.

[!NOTE]
For running the following steps you need to set environment variables from `.env` file based on your needs.

```bash
docker run --port 9092:9092 apache/kafka:3.9.0
```

```bash
docker run --port 9200:9200 elasticsearch:7.17.26
```

```bash
cd producer && pip install -r rquirements.txt && python producer.py
```

```bash
cd consumer && pip install -r rquirements.txt && python consumer.py
```

```bash
cd api && pip install -r rquirements.txt && fastapi dev run
```
