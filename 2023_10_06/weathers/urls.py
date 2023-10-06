from django.urls import path
from . import views

app_name = 'weathers'
urlpatterns = [
    path('', views.index),
    path('problem1/', views.problem1, name='problem1'), # 다운로드 받은 데이터(.csv 출력)
    path('problem2/', views.problem2, name='problem2'), # 일 별 온도 비교를 위한 라인 그래프 출력
    path('problem3/', views.problem3, name='problem3'), # 월 별 온도 비교를 위한 라인 그래프 출력
    path('problem4/', views.problem4, name='problem4'), # 기상 현상 발생 횟수 히스토그램 출력
]
