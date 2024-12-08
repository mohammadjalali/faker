## FAKER

This is a simple application to stream fake data from kafka to elasticsearch.
The application is made of `producer`, `consumer`, `apache kafka`, and `elasticsearch`.

- The producer gets data form <https://fakerapi.it/api/v2/texts?_quantity=100&_locale=fa_IR>
  and puts to `Kafka`.

- The consumer reads data from `Kafka` and puts data to `Elasticsearch`.

- The api can tag the contents and filter the contents of `Elasticsearch`.
  You can see <http://localhost:8000/docs> to findout what apis you can use.

- For running the whole project, just run the command below.

```bash
docker compose up -d
```
