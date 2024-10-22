# articleRating
This project is a simplified rating application for an article website


# Project Setup Guide

## Kafka Operations

### Create Kafka Topic "vote"

1. Ensure Kafka & Zookeeper are running.

2. Create the topic:
   ```bash
   docker exec -it <kafka_container_name> /opt/kafka/bin/kafka-topics.sh --create --topic vote --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
   ```

### View Messages on "vote" Topic

1. Access the Kafka container:
   ```bash
   docker exec -it <kafka_container_name> /bin/bash
   ```

2. Use Kafka console consumer:
   ```bash
   /opt/kafka/bin/kafka-console-consumer.sh --topic vote --bootstrap-server localhost:9092 --from-beginning
   ```

## Django User Authentication

### Create User Auth Token

1. Open Django shell:
   ```bash
   python manage.py shell
   ```

2. Generate token:
   ```python
   from django.contrib.auth.models import User
   from rest_framework.authtoken.models import Token

   user = User.objects.get(username='your_username')  # Replace with username
   token, created = Token.objects.get_or_create(user=user)
   print(f"Token: {token.key}")
   ```

Ensure your Django project is set up for token authentication with `rest_framework.authtoken` and `TokenAuthentication`.


## API Request

### Add a Vote using `curl`

To add a vote from `user2` with a score of 3 for `article1`, use the following `curl` command:

```bash
curl -X POST http://localhost:8000/articles/<article_id>/vote/ \
     -H "Authorization: Token <user_auth_token>" \
     -H "Content-Type: application/json" \
     -d '{"score": 3}'
```
