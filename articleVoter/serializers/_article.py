
from rest_framework import serializers

from django.core.exceptions import ObjectDoesNotExist

from articleVoter.models import Article, Rating


class ArticleSerializer(serializers.ModelSerializer):
    user_score = serializers.SerializerMethodField()

    def get_user_score(self, article: Article):
        try:
            latest_rating = Rating.objects.filter(
                user=self.context.get('user'),
                article_id=article
            ).order_by('-submit_time').first()

            if latest_rating is not None:
                return latest_rating.score
            else:
                return 0
        except ObjectDoesNotExist:
            return 0

    class Meta:
        model = Article
        fields = (
            'id',
            'title',
            'text',
            'mean_score',
            'count_score',
            'user_score',
        )
