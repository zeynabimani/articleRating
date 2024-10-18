from django.db import models


class ArticleScore(models.Model):
    mean_score = models.PositiveIntegerField()
    calculate_time = models.DateTimeField()

    class Meta:
        abstract = True


class Article(ArticleScore):
    title = models.CharField(max_length=250)
    text = models.TextField()
