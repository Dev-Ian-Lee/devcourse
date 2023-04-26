from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import F
from .models import *

def index(request):
    # 모델에서 데이터를 가져와 템플릿으로 전달할 context 생성
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {"questions": latest_question_list}

    # 인자로 받은 request와 생성한 context를 사용해 템플릿 호출
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    # 찾는 객체가 있으면 객체를 찾아오고, 없으면 404에러 반환
    question = get_object_or_404(Question, pk = question_id)

    return render(request, "polls/detail.html", {"question" : question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk = question_id)

    try:
        # 사용자가 form에 입력한 값 가져오기
        selected_choice = question.choice_set.get(pk = request.POST["choice"])

    # KeyError: 사용자가 아무런 선택도 하지 않고 form을 제출할 경우 발생
    # Choice.DoesNotExist: 존재하지 않는 Choice 객체를 get()할 경우 발생
    except (KeyError, Choice.DoesNotExist) : 
        return render(request, "polls/detail.html", {"question": question, "error_message" : f'선택이 없습니다. id = {request.POST["choice"]}'})

    else:
        # DB에서 votes의 값을 불러와 1 증가
        # 여러 명의 사용자가 동시에 연산하는 경우도 반영 가능
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

        # result 페이지로 redirect
        return HttpResponseRedirect(reverse("polls:result", args = (question_id, )))
    
def result(request, question_id):
    question = get_object_or_404(Question, pk = question_id)

    return render(request, "polls/result.html", {"question": question})