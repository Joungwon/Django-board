from django.contrib import admin
from .models import Movie,Comment

# Register your models here.
admin.site.register(Movie)
admin.site.register(Comment) #댓글 생성시 comment모델을 admin site에 등록