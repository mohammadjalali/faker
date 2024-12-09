## FAKER the MAKER

This is a simple application to stream fake data from kafka to elasticsearch.
The application is made of `producer`, `consumer`, `apache kafka`, and `elasticsearch`.

- The producer gets data from <https://fakerapi.it/api/v2/texts?_quantity=100&_locale=fa_IR>
  and puts to `Kafka`.

- The consumer reads data from `Kafka` and puts data to `Elasticsearch`.

- The api can tag the contents and filter the contents of `Elasticsearch`.
  You can see <http://localhost:8000/docs> to findout what apis you can use.

- The project is not completed. for completing the project the following steps need to get done.

- [ ] An API to tag the elasticsearch contents.

- To run the project using docker compose, you can run `docker compose up -d`.
  The environment variables in `.env` file is set based on docker compose configurations.
