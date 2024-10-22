import json
import logging
import time

from django.core.management.base import BaseCommand
from django.conf import settings
from articleVoter.utils.kafka import kafka_consumer

from articleVoter.models import Rating

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "insert vote kafka messages in db in batch operation"

    def handle(self, *args, **options):
        try:
            consumer = kafka_consumer()
            kafka_config = settings.KAFKA_CONFIG
            while True:
                ratings = []
                start_time = time.time()

                for message in consumer:
                    json_message = json.loads(message.value)
                    ratings.append(Rating(article_id=json_message.get('article'), user_id=json_message.get('user'), score=json_message.get('score')))
                    if len(ratings) >= kafka_config.get('CONSUMER_COUNT_THRESHOLD'):
                        break
                    if (time.time() - start_time) * 1000 >= kafka_config.get('CONSUMER_TIME_THRESHOLD'):
                        break

                consumer.commit()
                Rating.objects.bulk_create(ratings)            
        except Exception as e:
            logger.error(f"An error occurred during reading from kafka: {e}")
        finally:
            consumer.close()
