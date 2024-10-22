from rest_framework import serializers

from articleVoter.utils.exceptions import BadRequestError


class ArticleVoteSerializer(serializers.Serializer):
    score = serializers.IntegerField(required=True)

    def validate_score(self, value):
        if not 0 <= value <= 5:
            raise BadRequestError('Score is invalid. Please enter number between 0 and 5.')
        return value
