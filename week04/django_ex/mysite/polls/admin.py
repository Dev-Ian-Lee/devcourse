from django.contrib import admin
from .models import *

# Register your models here.

# Choice 객체를 Question 객체 페이지에서 관리
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

# Question 객체 커스터마이징
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("질문 섹션", {"fields" : ["question_text"]}),

        # collapse: 숨김 기능
        ("생성일", {"fields" : ["pub_date"], "classes" : ["collapse"]})
    ]

    # 목록 페이지 출력 형식
    list_display = ("question_text", "pub_date", "was_published_recently")

    # 생성일은 관리자가 수정하는 것이 아니고, 글이 생성될 때의 시각이 고정
    readonly_fields = ["pub_date"]

    inlines = [ChoiceInline]

    # 생성일 기준 정렬 필터
    list_filter = ["pub_date"]

    # Question과 Choice의 텍스트로 검색
    search_fields = ["question_text", "choice__choice_text"]

admin.site.register(Question, QuestionAdmin)