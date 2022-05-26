from django import forms
from .models import Movie, Comment, Score



class MovieForm(forms.ModelForm):

    class Meta:
        model = Movie
        exclude=('user', 'like_users', )

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content',)
        
class ScoreForm(forms.ModelForm):

    class Meta:
        model = Score
        fields = ('star', )