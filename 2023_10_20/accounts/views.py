from django.shortcuts import redirect, render
from .forms import CustomuserCreationForm
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


# Create your views here.
@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect("boards:index")
    
    # Method가 Get일 때와 POST일 때
    # 실제로 회원 가입 진행
    if request.method == "POST":
        form = CustomuserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("boards:index")
    # 회원가입 페이지를 보여준다.
    else:
        form = CustomuserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect("boards:index")
    
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("boards:index")
    
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


# 세션 데이터를 삭제하네 -> POST 요청
@require_POST
def logout(request):
    # 로그인 된 사용자만 로그아웃
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect("boards:index")

def profile(request, username):
    user = get_user_model()
    person = user.objects.get(username=username)
    context = {
        'person' : person,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def follow(request, user_pk, board_pk):
    per = get_user_model()
    person = per.objects.get(pk=user_pk)
    if person != request.user:
        if request.user in person.followers.all():
            person.followers.remove(request.user)
        else:
            person.followers.add(request.user)
    return redirect('boards:detail', board_pk)