from rest_framework import generics, permissions
from polls.models import Question
from polls_api.serializers import *
from django.contrib.auth.models import User
from .permission import IsOwnerOrReadOnly

class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    # 로그인하지 않았다면 질문 작성 불가
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # 질문 생성 시 작성자 저장
    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)

class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    # 질문 작성자가 아니면 질문 수정 불가
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer