from django.shortcuts import render, redirect,get_object_or_404
from .forms import MovieForm, CommentForm
from .models import Movie, Comment
from django.views.decorators.http import require_POST,require_GET,require_http_methods
from django.contrib.auth.decorators import login_required #로그인상태에서만 보이게
# Create your views here.
@require_GET
def index(request): #메인페이지
    movies = Movie.objects.all()
    context ={
        'movies':movies
    }
    return render(request, 'movies/index.html',context)

@require_GET
def detail(request,pk):  #게시글 세부페이지
    movie = Movie.objects.get(pk=pk) #일반적인 경우
    # movie = get_object_or_404(Movie,pk=pk) #http에서 디테일페이지로 들어가려할떄 오류 -> 접근불가처리
    
    comment_form =CommentForm()
    comments = movie.comment_set.all()  #작성한 댓글 목록 출력할때 추가
    context ={
        'movie' :movie,
        'comment_form':comment_form,
        'comments':comments,
    }
    return render(request, 'movies/detail.html',context)

@login_required    # 방법1   - 이방법으로 로그인했으면 쿼리스트링 위치로 바로 이동시켜준다.
@require_http_methods(["GET", "POST"])
def create(request):  #게시글 생성
    # if request.user.is_authenticated: # 방법2 유저가 로그인했을경우만
    #     return redirect('accounts:login') #아닌경우 작성안되고 로그인 페이지로
    if request.method =='POST':
        form =MovieForm(request.POST, request.FILES)
        if form.is_valid():
            # movie=form.save() #일반
             # 모델에서 ForeignKey를 사용했을경우 null값을 가진 테이블 생성
            movie =form.save(commit=False)  # forms에서 유저정보만 안보이게 할때, 외래키 정보누락상태 
            movie.user =request.user  #null값 테이블을 유저 아이디 정보로 채워줌 
            movie.save() #다시 저장
            return redirect('movies:detail',movie.pk)
    else:
        form= MovieForm()
        context = {
            'form' : form
        }
        return render(request, 'movies/create.html',context)
    
@require_http_methods(["GET", "POST"])
def update(request,pk): #게시글 수정
    movie = Movie.objects.get(pk=pk)
    if request.method =="POST":
        form = MovieForm(request.POST ,  instance=movie)
        if form.is_valid:
            form.save()
            return redirect('movies:detail', movie.pk)

    else:
        form = MovieForm(instance=movie)
    context ={
        'movie' : movie,
        'form' : form
    }
    return render(request, 'movies/update.html',context)

@require_POST
def delete(request,pk):  #게시글 삭제
    # 요청한 사용자 =request.user / 게시글 작성자 = article.user
    movie = Movie.objects.get(pk=pk)
    # if request.user == movie.user:  # 동일한 유저일경우만 삭제 가능
    #     movie.delete()
    movie.delete()
    return redirect('movies:index')


def comments_create(request,pk): #댓글 생성
    if not request.user.is_authenticated:   # 로그인 안했을경우 로그인창으로
        return redirect('accounts:login')  
    movie = Movie.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.movie =movie
        comment.user = request.user
        comment.save()
    return redirect('movies:detail',movie.pk)

def comments_delete(request,movie_pk,comment_pk): #댓글 삭제
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('movies:detail',movie_pk)

@require_POST
def likes(request,movie_pk): #좋아요 기능
    if request.user.is_authenticated:
        movie =Movie.objects.get(pk=movie_pk)
        if movie.like_users.filter(pk=request.user.pk).exists(): #exists() = queryset에 결과가 포함되어있으면 True 반환
        # if request.user in movie.like_users.all(): 같은말이지만 효율이 위에꺼가 낫다.
            movie.like_users.remove(request.user)
        else:
            movie.like_users.add(request.user)
        return redirect('movies:index')
    return redirect('accounts:login')