from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Board, Comment
from .forms import BoardForm
# Create your views here.
# @login_required
def index(request):
    boards = Board.objects.order_by('-pk')
    context = {'boards': boards}
    return render(request, 'boards/index.html', context)

@login_required
def create(request):
    # if not request.user.is_authenticated:
    #     return redirect('boards:index')
    if request.method == 'POST':
        board_form = BoardForm(request.POST)
        if board_form.is_valid():
            # title = board_form.cleaned_data.get('title')
            # content = board_form.cleaned_data.get('content')
            # board = Board(title=title, content=content)
            # board.user = request.user
            # board.save()
            board = board_form.save(commit=False)
            board.user = request.user
            board.save()
            return redirect(board)
    else:
        board_form = BoardForm()
    context = {'board_form': board_form}
    return render(request, 'boards/form.html', context)
    
def detail(request, board_pk):
    # board = Board.objects.get(pk=board_pk)
    board = get_object_or_404(Board, pk=board_pk)
    if request.method == "POST":
        comment = Comment(comment=request.POST.get('comment'), writer=request.user, board_id=board_pk)
        comment.save()
        return redirect('boards:detail', board_pk)
    else:
        board.hit += 1
        board.save()
    comments = board.comment_set.all()
    context = {'board': board, 'comments': comments}
    return render(request, 'boards/detail.html', context)

def delete(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if request.method == 'POST':
        board.delete()
        return redirect('boards:index')
    else:
        return redirect(board)

def comment_delete(request, board_pk, comment_pk):
    board = Board.objects.get(pk=board_pk)
    comment = board.comment_set.get(pk=comment_pk)
    comment.delete()
    return redirect('boards:detail', board_pk)

def update(request, board_pk):
    # 1. board_pk에 해당하는 오브젝트를 가져온다.
    #    - 없으면, 404 에러.
    #    - 있으면, board = Board.objects.get(pk=board_pk) 와 동일.
    board = get_object_or_404(Board, pk=board_pk)
    # 2-1. POST 요청이면 (사용자가 form을 통해 데이터를 보내 준 것.)
    if request.method == 'POST':
        # 사용자 입력값(request.POST)을 BoardForm에 전달해주고,
        board_form = BoardForm(request.POST, instance=board)
        # 검증 (유효성 체크)
        if board_form.is_valid():
            # board.title = board_form.cleaned_data.get('title')
            # board.content = board_form.cleaned_data.get('content')
            # board.save()
            board = board_form.save()
            return redirect(board)
    # 2-2. GET 요청이면 (수정하기 버튼을 눌렀을 때)
    else:
        # BoardForm을 초기화(사용자 입력값을 넣어준 상태)
        board_form = BoardForm(instance=board) 
    # context에 담겨있는 board_form은 두가지 상황이 있다.
    # 1 - POST 요청에서 검증에 실패하였을 때, 오류 메세지가 포함된 상태
    # 2 - GET 요청에서 초기화된 상태
    context = {'board_form': board_form}
    return render(request, 'boards/form.html', context)










