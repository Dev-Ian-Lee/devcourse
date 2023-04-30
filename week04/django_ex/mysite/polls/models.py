from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User
import datetime

# Create your models here.

# 질문 모델
class Question(models.Model):
    # verbose_name: admin 페이지에서 출력될 이름
    question_text = models.CharField(max_length = 200, verbose_name = "질문")
    pub_date = models.DateTimeField(auto_now_add = True, verbose_name = "생성일")

    # owner라는 User 객체는 여러 개의 Question 객체를 가짐
    # User 객체에서 Question 객체를 접근할 때 "questions"라는 이름을 사용
    # owner가 삭제되면 Question 객체도 삭제(cascade)
    owner = models.ForeignKey("auth.User", related_name = "questions", on_delete = models.CASCADE, null = True)

    # 생성한 지 하루 이내인지 확인하는 메서드
    @admin.display(boolean = True, description = "최근 생성(하루 기준)")
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days = 1)

    def __str__(self):
        if self.was_published_recently():
            new_badge = 'NEW!!'

        else:
            new_badge = ''

        return f'{new_badge} 제목: {self.question_text}, 날짜: {self.pub_date}'

# 답변 모델
class Choice(models.Model):
    # Foreign Key를 사용해 질문 테이블과 관계 정의
    question = models.ForeignKey(Question, related_name = "choices", on_delete = models.CASCADE)

    choice_text = models.CharField(max_length = 200)
    votes = models.IntegerField(default = 0)

    def __str__(self):
        return f'[{self.question.question_text}] {self.choice_text}'
    
class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete = models.CASCADE)
    voter = models.ForeignKey(User, on_delete = models.CASCADE)

    class Meta:
        # 각 사용자가 하나의 질문에 한 번만 투표할 수 있도록 UNIQUE 제약조건 생성
        constraints = [
            models.UniqueConstraint(fields = ["question", "voter"], name = "unique_voter_for_questions")
        ]