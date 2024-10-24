# Article Rating Application

## Overview

This is a Django application designed for an article rating website. The core functionality is encapsulated within an app called `articleRating`, which features two primary models: `Article` and `Rating`. The application leverages the Django `auth` module for user management, ensuring integrated and secure user authentication.

## Features

- **Models**:
  - **Article**: Represents the articles users can rate.
  - **Rating**: Captures the ratings provided by users.

- **ViewSets**:
  - **Ratings Creation**: Insert a single record in `Rating` tabel.
  - **Articles Listing**: List articles with their ratings.

## Technology Stack

- **Kafka Integration**: 
  - Used to handle and store rating records efficiently.
  - Facilitates `bulk_create` to manage ratings due to the high load of requests.
  - Processes either batches of 1000 ratings or executes every 500 milliseconds to ensure data consistency.
  - To address immediate user feedback, client-side caching is recommended so users are not immediately aware of the asynchronous processing.

- **Redis Integration**: 
  - Used to handle article listing more efficiently.

- **Cron Job**:
  - A cron job is set up to compute the mean score for each article, running periodically to keep the data updated.

- **Dockerization**:
  - The project is fully containerized using Docker, allowing it to be deployed seamlessly across various environments, ensuring consistency in execution.


Further documentation for the various components and their interactions within the system is provided below.


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

## Cronjob

To calculate the mean score for articles, I have implemented a cron job that runs every 5 minutes. The frequency of this job can be adjusted based on our specific needs, as determined by the product manager.

Instead of updating individual ratings, each new rating is inserted into the database. This approach is favored due to the high volume of requests I handle. Using bulk_create for these insertions is more efficient and faster under heavy load.

When computing the mean score for each article, only the most recent score from each user is considered. This ensures that our calculations reflect the latest user evaluations for each article.


### Why Cron Instead of Kubernetes
Given the absence of a Kubernetes environment, I've used a traditional cron-based setup:

**Simplicity:** Easy to implement and manage without needing Kubernetes infrastructure.

**Familiarity:** Cronjobs are straightforward for those accustomed to Unix systems. 

**Flexibility:** Quickly adaptable for development and smaller-scale deployments.