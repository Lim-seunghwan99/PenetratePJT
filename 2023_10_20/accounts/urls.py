from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    # 회원가입
    path('signup/', views.signup, name='signup'),
    # 로그인
    path('login/', views.login, name='login'),
    # 로그아웃
    path('logout/', views.logout, name='logout'),
    # 프로필페이지
    path('profile/<username>/', views.profile, name='profile'),
    #구독 기능
    path('<int:user_pk>/follow/<int:board_pk>/', views.follow, name='follow'),
]
