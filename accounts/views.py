from django.shortcuts import render, redirect
# from .forms import UserForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.contrib.auth import login as auth_login # 재귀로 호출되지 않도록 하기 위해 auth_login으로 변경
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_http_methods

from .forms import UserCustomChangeForm, UserCustomCreationForm

# Create your views here.
def index(request):
    users = get_user_model().objects.all()
    context = {'users': users}
    return render(request, 'accounts/index.html', context)

def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    boards = user.board_set.all()
    context = {'user': user, 'boards': boards}
    return render(request, 'accounts/detail.html', context)

def signup(request):
    if request.user.is_authenticated:
        return redirect('boards:index')
    if request.method == 'POST':
        user_form = UserCustomCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            auth_login(request, user)
            messages.info(request, f'{user.username}님, 회원가입 성공!')
            return redirect('boards:index')
        messages.warning(request, '양식을 다시 확인해주세요.')
    else:
        user_form = UserCustomCreationForm()
    context = {'user_form': user_form}
    return render(request, 'accounts/signup.html', context)
    
def login(request):
    if request.user.is_authenticated:
        return redirect('boards:index')
    if request.method == 'POST':
        login_form = AuthenticationForm(request, request.POST) # 사용자의 쿠키 값을 받아오기 위해 request 인자를 추가, 사용자가 입력한 정보 + 서버에서 가져온 값을 비교
        if login_form.is_valid():
            auth_login(request, login_form.get_user()) # form에서 사용자와 관련된 정보만을 뽑아서 session을 만드는 함수
            return redirect('boards:index')
    else:
        login_form = AuthenticationForm()
    context = {'login_form': login_form}
    return render(request, 'accounts/login.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('boards:index')
    
@login_required
def signout(request):
    if request.method == 'POST':
        request.user.delete()
    return redirect('boards:index')
    
# @login_required
# @require_http_methods(["POST"]) # method가 없음을 나타내는 405코드를 보냄, 성공 시에는 200코드
# def signout(request):
#     request.user.delete()
#     return redirect('boards:index')


def update(request):
    # user_form = UserChangeForm()
    if request.method == 'POST':
        user_form = UserCustomChangeForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('boards:index')
    else:
        user_form = UserCustomChangeForm(instance=request.user)
    context = {'user_form':user_form}
    return render(request, 'accounts/update.html', context)
    
@login_required
def password(request):
    if request.method == 'POST':
        user_form = PasswordChangeForm(request.user, request.POST) # 순서 주의!
        if user_form.is_valid():
            user_form.save()
            update_session_auth_hash(request, user)
        return redirect('boards:index')
    else:
        user_form = PasswordChangeForm(request.user) # instance = 아님을 주의!
    context = {'user_form': user_form}
    return render(request, 'accounts/update.html', context)