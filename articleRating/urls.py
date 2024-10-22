from django.urls import include, re_path
from rest_framework import routers
from articleVoter.views import VoteViewSet

ID = r'(?P<id>\d{1,12})'


router = routers.SimpleRouter()
router.register('articles/{}/vote'.format(ID), VoteViewSet, basename='release')

urlpatterns = [
    re_path('', include((router.urls, 'mag'), namespace='mag')),
]
