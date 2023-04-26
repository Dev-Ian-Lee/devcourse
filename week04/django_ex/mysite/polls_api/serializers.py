from rest_framework import serializers
from polls.models import Question

class QuestionSerializer(serializers.ModelSerializer):
    # 메타 정보 기록
    class Meta:
        model = Question
        fields = ["id", "question_text", "pub_date"]