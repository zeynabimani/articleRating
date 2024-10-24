from django.urls import include, re_path
from rest_framework import routers
from articleVoter.views import ArticleViewSet, VoteViewSet

ID = r'(?P<id>\d{1,12})'


router = routers.SimpleRouter()
router.register('articles', ArticleViewSet, basename='article')
router.register('articles/{}/vote'.format(ID), VoteViewSet, basename='vote')

urlpatterns = [
    re_path('', include((router.urls, 'mag'), namespace='mag')),
]
