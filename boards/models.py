from django.db import models
from django.urls import reverse
# from django.contrib.auth.models import User # 사용하지 마세요
# from django.contrib.auth import get_user_model
from django.conf import settings # 가장 추천
#settings.AUTH_USER_MODEL로 쓸 것
# default 값이 'auth.User'

# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=10)
    content = models.TextField()
    hit = models.IntegerField(default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'<Board ({self.id})> : {self.title}'
        
    def get_absolute_url(self):
        return reverse('boards:detail', args=[self.pk])
        
        
class Comment(models.Model):
    comment = models.TextField()
    writer = models.CharField(max_length=10)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)