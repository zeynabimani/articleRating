from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from articleVoter.models import Article
from articleVoter.utils.kafka import produce_json_to_kafka
from articleVoter.serializers import ArticleVoteSerializer


class VoteViewSet(viewsets.GenericViewSet,
                  viewsets.mixins.CreateModelMixin):
    
    def create(self, request, *args, **kwargs):
        article = self.get_article(kwargs['id'])
        serializer = ArticleVoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = serializer.validated_data
        score = serializer_data.get('score')

        kafka_message = {
            'article': article.id,
            'user': request.user.id,
            'score': score,
        }
        produce_json_to_kafka(kafka_message)

        return Response({
            'type': 'success',
            'message': 'Score submited successfully',
        }, status=status.HTTP_201_CREATED)
    
    def get_article(self, id):
        return get_object_or_404(Article, id=id)
