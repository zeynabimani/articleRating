from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import OuterRef, Subquery, Avg, Count
from django.utils import timezone

from articleVoter.models import Article, Rating


class Command(BaseCommand):
    help = "update articles score"

    def handle(self, *args, **options):
        latest_ratings = Rating.objects.filter(
            article=OuterRef('article'),
            user=OuterRef('user')
        ).order_by('-id')

        latest_rating_per_user_article = Rating.objects.filter(
            id=Subquery(latest_ratings.values('id')[:1])
        )

        average_scores = latest_rating_per_user_article.values('article').annotate(
            avg_score=Avg('score'), cnt_score=Count('score')
        ).order_by('article')

        articles_to_update = []
        for entry in average_scores:
            try:
                article_instance = Article.objects.get(id=entry.get('article'))
                article_instance.mean_score = round(entry.get('avg_score', 0))
                article_instance.count_score = entry.get('cnt_score', 0)
                article_instance.score_calculate_time = timezone.now()
                articles_to_update.append(article_instance)
            except Article.DoesNotExist:
                continue

        with transaction.atomic():
            Article.objects.bulk_update(
                articles_to_update,
                ['mean_score', 'score_calculate_time', 'count_score']
            )
