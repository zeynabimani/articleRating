from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from articleVoter.models import Article


class Rating(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    score = models.PositiveIntegerField()
    submit_time = models.DateTimeField(default=timezone.now)
