from django.shortcuts import render, redirect
# from .forms import UserForm
from django.contrib.auth import login as auth_login # 재귀로 호출되지 않도록 하기 위해 auth_login으로 변경
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout

# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('boards:index')
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            auth_login(request, user)
            return redirect('boards:index')
    else:
        user_form = UserCreationForm()
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
    
def logout(request):
    auth_logout(request)
    return redirect('boards:index')