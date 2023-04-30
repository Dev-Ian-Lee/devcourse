from rest_framework import generics, permissions
from rest_framework import status
from rest_framework.response import Response
from polls.models import Question
from polls_api.serializers import *
from django.contrib.auth.models import User
from .permission import IsOwnerOrReadOnly, IsVoter

class VoteList(generics.ListCreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    # 내가 작성한 Vote만 목록으로 출력
    def get_queryset(self, *args, **kwargs):
        return Vote.objects.filter(voter = self.request.user)
    
    # 유효성 검사 하기 전에 voter를 설정하기 위해 perform_create()가 아닌 create()를 재정의
    def create(self, request, *args, **kwargs):
        new_data = request.data.copy()
        new_data["voter"] = request.user.id
        serializer = self.get_serializer(data = new_data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class VoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsVoter]

    def perform_update(self, serializer):
        serializer.save(voter = self.request.user)

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