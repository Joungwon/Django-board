from django import forms
from .models import Movie,Comment

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        # fields = '__all__'
        exclude = ('user','like_users') #게시글 생성시 유저정보입력은 안보이게

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields =('content',)  #방법1
        # exclude =('article',)   #방법2  예외처리