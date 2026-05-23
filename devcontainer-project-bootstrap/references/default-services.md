# Default Services

Use official images, official default ports, persistent data under `./data/<service-name>`, and healthchecks when useful.

| Service | Port | Data path |
| --- | ---: | --- |
| PostgreSQL | 5432 | `./data/postgresql` |
| MySQL | 3306 | `./data/mysql` |
| MariaDB | 3306 | `./data/mariadb` |
| Redis | 6379 | `./data/redis` |
| RabbitMQ | 5672 | `./data/rabbitmq` |
| RabbitMQ Management | 15672 | `./data/rabbitmq` |
| Kafka | 9092 | `./data/kafka` |
| Zookeeper | 2181 | `./data/zookeeper` |
| MinIO API | 9000 | `./data/minio` |
| MinIO Console | 9001 | `./data/minio` |
| MongoDB | 27017 | `./data/mongodb` |
| OpenSearch | 9200 | `./data/opensearch` |
| Prometheus | 9090 | `./data/prometheus` |
| Grafana | 3000 | `./data/grafana` |
| NATS | 4222 | `./data/nats` |

Rules:

- Never generate real secrets.
- Put only local example values in `.env.example`.
- Use official default ports unless explicitly overridden.
- Use service names exactly as lowercase canonical names.
- Add only requested or architecturally required services.
- Create writable service data source directories before container startup.
- Persist service data under `./data/<service-name>`.
- Do not chown service-owned data directories to the development user unless the service image documentation says that UID/GID is expected.
- Document service image UID/GID expectations when they matter. For example, RabbitMQ commonly runs with an internal service UID such as `999`; `data/rabbitmq` may need to match the RabbitMQ image, not the development user.
