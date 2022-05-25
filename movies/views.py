from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from .models import Director, Movie, Comment, Actor, Score
from .forms import MovieForm, CommentForm, ScoreForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.http import JsonResponse
from django.db.models import Avg

# Create your views here.
def index(request):
    movies = Movie.objects.all()
    context={
        'movies':movies
    }

    return render(request, 'movies/index.html',context)

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
    # scores= get_list_or_404(Score)
    
    comment_form=CommentForm()
    comments=movie.comment_set.all()
    comments_num = len(movie.comment_set.all())
    
    # score_list=movie.score_set.all()
    # score_form=ScoreForm(request.POST, instance=scores)
    
    scores_temp=movie.score_set.aggregate(Avg('star'))
    scores_avg=str(scores_temp['star__avg'])[:3]
    scores_num= len(movie.score_set.all())
    
    # if score_list.user.filter(pk=request.user.pk).exists():
    #     score_list.user.remove(request.user)
    # else:
    #     score_list.user.add(request.user)
        
    context = {
        'movie':movie,
        'directors':directors,
        'actors':actors,
        # 'scores':scores,
        
        'comment_form':comment_form,
        'comments':comments,
        'comments_num':comments_num,
        
        # 'score_form':score_form,
        # 'score_list':score_list,
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

@require_POST
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