from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from .models import Director, Movie, Comment, Actor, Score
from .forms import MovieForm, CommentForm, ScoreForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.http import JsonResponse
from django.db.models import Avg

# Create your views here.
def index(request):
    # 알고리즘 1 : 최신 순
    # 5번부터 올리는 것으로 만들기
    movies = Movie.objects.order_by('-release_date').filter(vote_average__gt=7)
    # 알고리즘 2 : 평점 순
    movies2 = Movie.objects.order_by('-vote_average')
    context={
        'movies':movies,
        'movies2':movies2
    }
    return render(request, 'movies/index.html',context)

def search(request):
    search=request.GET.get('search')
    movies = Movie.objects.filter(title__contains=search)
    movies2 = Movie.objects.filter(overview__contains=search)
    
    movies_len_1= len(movies) if len(movies) < 40 else 40
    movies_len_4_1_temp = len(movies)//4 if len(movies)%4 == 0 else len(movies)//4 + 1
    movies_len_4_1= movies_len_4_1_temp if movies_len_4_1_temp < 10 else 10
    
    movies_len_2= len(movies2) if len(movies2) < 40 else 40
    movies_len_4_2_temp = len(movies2)//4 if len(movies2)%4 == 0 else len(movies2)//4 + 1
    movies_len_4_2= movies_len_4_2_temp if movies_len_4_2_temp < 10 else 10
    
    context={
        'search':search,
        'movies':movies,
        'movies2':movies2,
        'movies_len_1':movies_len_1,
        'movies_len_4_1':movies_len_4_1,
        'movies_len_2':movies_len_2,
        'movies_len_4_2':movies_len_4_2,
    }
    return render(request, 'movies/search.html',context)

    # 1. 최신순 -> 평점 순서 부여
    # 2. 평점순 -> 전체 goty
    # 3. 랜덤
    # 4. 현재 시간 이후 또는 이전 영화
    # 5. 장르별(식상할듯)
    # 6. 감독, 배우를 검색을 통해서 영화 가져올 수 있도록
    
def recommend(request, user_pk):
    movies = Movie.objects.order_by('?')
    
    
    director = Director.objects.filter(like_users__exact=user_pk).order_by("?").first()
    director_temp = len(Director.objects.filter(like_users__exact=user_pk))
    if director:
        movies2 = Movie.objects.filter(directors=director.id)
    else:
        movies2 = ''
        
    actor = Actor.objects.filter(like_users__exact=user_pk).order_by("?").first()
    actor_temp = len(Actor.objects.filter(like_users__exact=user_pk))
    if actor:
        movies3 = Movie.objects.filter(actors=actor.id)
    else:
        movies3 = ''
    
    movies_total = Movie.objects.all()
    
    scores = Score.objects.filter(user_id=user_pk).order_by('-star')
    scores_temp = len(Score.objects.filter(user_id=user_pk))
    
    if scores:
        scores_movie = scores.values('movie_id')[0]['movie_id']
        scores_movie_genre = Movie.objects.filter(pk=scores_movie).values()[0]['genre']
        movies4 = Movie.objects.filter(genre__contains=scores_movie_genre)
    else:
        scores_movie = ''
        scores_movie_genre = ''
        movies4 = ''
    
    scores2 = Score.objects.filter(user_id=user_pk)
    dict = {'액션':0, '모험':0, '애니메이션':0, '코미디':0, '범죄':0, '다큐멘터리':0, '드라마':0, '가족':0, '판타지':0, '역사':0, '공포':0, '음악':0, '미스터리':0, '로맨스':0, 'SF':0, 'TV 영화':0, '스릴러':0, '전쟁':0, '서부':0}
    for score in scores2:
        if score.star >= 4.0:
            tmp = Movie.objects.filter(pk=score.movie_id)
            dict[tmp.values()[0]['genre']] += 1
    maxV = 0
    genre = ''
    for key, value in dict.items():
        if value > maxV:
            maxV = value
            genre = key
    movies5 = Movie.objects.filter(genre__contains=genre)
    
    movies_len_1= len(movies) if len(movies) < 40 else 40
    movies_len_4_1_temp = len(movies)//4 if len(movies)%4 == 0 else len(movies)//4 + 1
    movies_len_4_1= movies_len_4_1_temp if movies_len_4_1_temp < 10 else 10
    
    movies_len_2= len(movies2) if len(movies2) < 40 else 40
    movies_len_4_2_temp = len(movies2)//4 if len(movies2)%4 == 0 else len(movies2)//4 + 1
    movies_len_4_2= movies_len_4_2_temp if movies_len_4_2_temp < 10 else 10

    movies_len_3= len(movies3) if len(movies3) < 40 else 40
    movies_len_4_3_temp = len(movies3)//4 if len(movies3)%4 == 0 else len(movies3)//4 + 1
    movies_len_4_3= movies_len_4_3_temp if movies_len_4_3_temp < 10 else 10
    
    movies_len_4= len(movies4) if len(movies4) < 40 else 40
    movies_len_4_4_temp = len(movies4)//4 if len(movies4)%4 == 0 else len(movies4)//4 + 1
    movies_len_4_4= movies_len_4_4_temp if movies_len_4_4_temp < 10 else 10
    
    movies_len_5= len(movies5) if len(movies5) < 40 else 40
    movies_len_4_5_temp = len(movies5)//4 if len(movies5)%4 == 0 else len(movies5)//4 + 1
    movies_len_4_5= movies_len_4_5_temp if movies_len_4_5_temp < 10 else 10
    
    
    context={
        'maxV':maxV,
        'genre':genre,
        'movies_total':movies_total,
        'scores_temp':scores_temp,
        'scores_movie_genre':scores_movie_genre,
        'director_temp':director_temp,
        'actor_temp':actor_temp,
        'actor':actor,
        'director':director,
        'movies':movies,
        'movies2':movies2,
        'movies3':movies3,
        'movies4':movies4,
        'movies5':movies5,
        'movies_len_1':movies_len_1,
        'movies_len_4_1':movies_len_4_1,
        'movies_len_2':movies_len_2,
        'movies_len_4_2':movies_len_4_2,
        'movies_len_3':movies_len_3,
        'movies_len_4_3':movies_len_4_3,
        'movies_len_4':movies_len_4,
        'movies_len_4_4':movies_len_4_4,
        'movies_len_5':movies_len_5,
        'movies_len_4_5':movies_len_4_5,
    }
    return render(request, 'movies/recommend.html',context)

@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user
            movie.save()
            return redirect('movies:detail', movie.pk)
    
    else:
        form=MovieForm()
    context = {
        'form':form,
    }
    return render(request, 'movies/create.html', context)


def detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    actors = get_list_or_404(Actor)
    directors = get_list_or_404(Director)
    
    movie_actors = movie.actors.all()
    movie_directors = movie.directors.all()
    
    comment_form=CommentForm()
    comments=movie.comment_set.all()
    comments_num = len(movie.comment_set.all())

    scores=movie.score_set.all()
    scores_user_temp=movie.score_set.aggregate(Avg('star'))
    scores_user=scores_user_temp['star__avg']
    scores_avg=str(scores_user_temp['star__avg'])[:3]
    scores_num=len(movie.score_set.all())
    
    context = {
        'movie':movie,
        'directors':directors,
        'actors':actors,
        'scores':scores,
        
        'movie_actors':movie_actors,
        'movie_directors': movie_directors,
        
        'comment_form':comment_form,
        'comments':comments,
        'comments_num':comments_num,
        
        'scores_user':scores_user,
        'scores_avg':scores_avg,
        'scores_num':scores_num,
    }
    return render(request, 'movies/detail.html', context)

@require_POST
def likes(request, movie_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)

        if movie.like_users.filter(pk=request.user.pk).exists():
            movie.like_users.remove(request.user)
            isLiked = False
        else:
            movie.like_users.add(request.user)
            isLiked = True
        context = {
            'isLiked': isLiked,
            'likedCount': movie.like_users.count(),
        }
        return JsonResponse(context)
    return redirect('accounts:login')

@login_required
@require_http_methods(['GET', 'POST'])
def update(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method=='POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            movie = form.save()
            return redirect('movies:detail', movie.pk)
    else:
        form = MovieForm(instance=movie)
    context={
        'movie':movie,
        'form':form,
    }
    return render(request, 'movies/update.html', context)


def delete(request, pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=pk)
        movie.delete()
    return redirect('movies:index')


@require_POST
def comments_create(request, pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment=comment_form.save(commit=False)
            comment.movie=movie
            comment.user = request.user
            comment.save()
        return redirect('movies:detail', movie.pk)
    return redirect('accounts:login')


@require_POST
def comments_delete(request, movie_pk, comment_pk):
    if request.user.is_authenticated:
        comment=get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('movies:detail', movie_pk)


@require_POST
def likes(request, movie_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)

        if movie.like_users.filter(pk=request.user.pk).exists():
            movie.like_users.remove(request.user)
            isLiked = False
        else:
            movie.like_users.add(request.user)
            isLiked = True
        context = {
            'isLiked': isLiked,
            'likedCount': movie.like_users.count(),
        }
        return JsonResponse(context)
    return redirect('accounts:login')


@require_POST
def director_likes(request, director_pk):
    if request.user.is_authenticated:
        director = get_object_or_404(Director, pk=director_pk)
        if director.like_users.filter(pk=request.user.pk).exists():
            director.like_users.remove(request.user)
            isLiked = False
        else:
            director.like_users.add(request.user)
            isLiked = True
        context = {
            'isLiked': isLiked,
            'likedCount': director.like_users.count(),
        }
        return JsonResponse(context)
    return redirect('accounts:login')


@require_POST
def actor_likes(request, actor_pk):
    if request.user.is_authenticated:
        actor = get_object_or_404(Actor, pk=actor_pk)
        if actor.like_users.filter(pk=request.user.pk).exists():
            actor.like_users.remove(request.user)
            isLiked = False
        else:
            actor.like_users.add(request.user)
            isLiked = True
        context = {
            'isLiked': isLiked,
            'likedCount': actor.like_users.count(),
        }
        return JsonResponse(context)
    return redirect('accounts:login')


@require_POST
def scores_create(request, pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=pk)
        score_form = ScoreForm(request.POST)
        if score_form.is_valid():
            score=score_form.save(commit=False)
            score.movie=movie
            score.user = request.user
            score.save()
        return redirect('movies:detail', movie.pk)
    return redirect('accounts:login')


@require_POST
def scores_delete(request, movie_pk, score_pk):
    if request.user.is_authenticated:
        score=get_object_or_404(Score, pk=score_pk)
        if request.user == score.user:
            score.delete()
    return redirect('movies:detail', movie_pk)


@require_POST
def scores_update(request, movie_pk, score_pk):
    if request.user.is_authenticated:
        # 삭제한다
        score=get_object_or_404(Score, pk=score_pk)
        if request.user == score.user:
            score.delete()
        # 새로 추가한다. 
        movie = get_object_or_404(Movie, pk=movie_pk)
        score_form = ScoreForm(request.POST)
        if score_form.is_valid():
            score=score_form.save(commit=False)
            score.movie=movie
            score.user = request.user
            score.save()
        return redirect('movies:detail', movie_pk)
    return redirect('accounts:login')