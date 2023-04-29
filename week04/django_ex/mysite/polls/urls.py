from django.urls import path
from . import views
from .views import *

# 템플릿에서 urls.py의 메서드를 호출할 때 사용할 app_name
app_name = "polls"

urlpatterns = [
    # 'polls/'로 요청이 들어올 경우, index 페이지 출력
    path('', views.index, name = "index"),

    # int 타입의 Query String이 들어온 경우, detail 페이지 출력
    path('<int:question_id>/', views.detail, name = "detail"),
    path('<int:question_id>/vote/', views.vote, name = "vote"),
    path('<int:question_id>/result', views.result, name = "result"),
    path('signup/', SignUpView.as_view())
]