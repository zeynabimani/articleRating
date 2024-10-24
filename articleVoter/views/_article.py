import pickle
from rest_framework import viewsets
from rest_framework.pagination import CursorPagination

from django.core.cache import cache
from django.conf import settings

from articleVoter.serializers import ArticleSerializer
from articleVoter.models import Article


# CURSUR_REDIS_KEY = "articles_cursor_{cursor}"
ARTICLE_REDIS_KEY = "articles_{article_id}"

class RedisCursorPagination(CursorPagination):
    page_size = settings.ARTICLE_PAGE_SIZE
    ordering = '-id'

    def paginate_queryset(self, queryset, request, view=None):
        # cursor_key = CURSUR_REDIS_KEY.format(cursor=request.query_params.get('cursor', 'start'))
        # article_ids = cache.get(cursor_key)
        # if not article_ids:
        #     queryset_ids = queryset.values_list('id', flat=True)
        #     paginated_queryset = super().paginate_queryset(queryset_ids, request, view)

        #     article_ids = list(paginated_queryset)
        #     cache.set(cursor_key, pickle.dumps(article_ids), settings.REDIS_ARTICLE_TTL)
        # else:
        #     article_ids = pickle.loads(article_ids)

        queryset_ids = queryset.values_list('id', flat=True)
        paginated_queryset = super().paginate_queryset(queryset_ids, request, view)
        article_ids = list(paginated_queryset)

        articles = []
        for article_id in article_ids:
            article_key = ARTICLE_REDIS_KEY.format(article_id=article_id)
            cached_article = cache.get(article_key)

            if cached_article:
                articles.append(pickle.loads(cached_article))
            else:
                try:
                    article = Article.objects.get(id=article_id)
                    cache.set(article_key, pickle.dumps(article), settings.REDIS_ARTICLE_TTL)
                    articles.append(article)
                except Article.DoesNotExist:
                    continue

        return articles


class ArticleViewSet(viewsets.GenericViewSet,
                     viewsets.mixins.ListModelMixin):

    serializer_class = ArticleSerializer
    pagination_class = RedisCursorPagination
    queryset = Article.objects.all()

    def list(self, request, *args, **kwargs):
        articles = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(articles, many=True, context={'user': request.user})
        return self.get_paginated_response(serializer.data)
