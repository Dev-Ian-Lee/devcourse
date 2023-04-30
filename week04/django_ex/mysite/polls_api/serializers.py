from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from polls.models import Question, Choice, Vote
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class VoteSerializer(serializers.ModelSerializer):
    # 질문에 대해 유효한 답변을 선택했는지 검증
    def validate(self, attrs):
        if attrs["choice"].question.id != attrs["question"].id:
            raise serializers.ValidationError("Question과 Choice의 조합이 맞지 않습니다.")
        
        return attrs

    class Meta:
        model = Vote
        fields = ["id", "question", "choice", "voter"]
        validators = [
            UniqueTogetherValidator(
            queryset = Vote.objects.all(),
            fields = ["question", "voter"]
            )
        ]

class ChoiceSerializer(serializers.ModelSerializer):
    votes_count = serializers.SerializerMethodField()

    class Meta:
        model = Choice
        fields = ["choice_text", "votes_count"]

    def get_votes_count(self, obj):
        # 각 선택지의 투표 개수
        return obj.vote_set.count()

class QuestionSerializer(serializers.ModelSerializer):
    # 질문 작성자의 이름 표시
    owner = serializers.ReadOnlyField(source = "owner.username")
    choices = ChoiceSerializer(many = True, read_only = True)

    class Meta:
        model = Question
        fields = ["id", "question_text", "pub_date", "owner", "choices"]

class UserSerializer(serializers.ModelSerializer):
    # User의 Question 객체를 HyperLinkedKeyRelatedField로 연결해 링크 제공
    questions = serializers.HyperlinkedRelatedField(many = True, read_only = True, view_name = "question-detail")

    class Meta:
        model = User
        fields = ["id", "username", "questions"]

class RegisterSerializer(serializers.ModelSerializer):
    # 패스워드 검증
    password = serializers.CharField(write_only = True, required = True, validators = [validate_password])
    password2 = serializers.CharField(write_only = True, required = True)

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "두 패스워드가 일치하지 않습니다."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(username = validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()

        return user

    class Meta:
        model = User
        fields = ["username", "password", "password2"]