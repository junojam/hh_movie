from django import forms
from .models import Article, ArticleComment


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        exclude = ('user', )

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = ArticleComment
        # exclude = ('article', )
        fields = ('content',)