from django.urls import path
from . import views

urlpatterns = [
    # 'polls/'로 요청이 들어올 경우, index 페이지 반환
    path('', views.index, name = "index"),
    path('some_url', views.some_url),
]