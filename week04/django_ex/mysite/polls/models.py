from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

# 질문 모델
class Question(models.Model):
    question_text = models.CharField(max_length = 200)
    pub_date = models.DateTimeField('date published')

    # 생성한 지 하루 이내인지 확인하는 메서드
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
    question = models.ForeignKey(Question, on_delete = models.CASCADE)

    choice_text = models.CharField(max_length = 200)
    votes = models.IntegerField(default = 0)

    def __str__(self):
        return f'[{self.question.question_text}] {self.choice_text}'