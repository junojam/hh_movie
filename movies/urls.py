from django.urls import path
from . import views

app_name='movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    
    
    path('<int:movie_pk>/likes/', views.likes, name='likes'),
    path('<int:director_pk>/director_likes/', views.director_likes, name='director_likes'),
    path('<int:actor_pk>/actor_likes/', views.actor_likes, name='actor_likes'),
    
    path('<int:pk>/comments/', views.comments_create, name='comments_create'),
    path('<int:pk>/scores/', views.scores_create, name='scores_create'),
    
    path('<int:movie_pk>/comments/<int:comment_pk>/delete/', views.comments_delete, name='comments_delete'),
    path('<int:movie_pk>/scores/<int:score_pk>/delete/', views.scores_delete, name='scores_delete'),
    path('<int:movie_pk>/scores/<int:score_pk>/update/', views.scores_update, name='scores_update'),
]