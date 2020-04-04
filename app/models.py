from django.db import models

# Create your models here.

class User(models.Model):
    SEX = (
        ('male', '男性'),
        ('female', '女性')
    )
    nickname = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)
    sex = models.CharField(max_length=6, choices=SEX)
    age = models.IntegerField(default=18)
    created = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(verbose_name='用户头像')
    pass

class Post(models.Model):
    title = models.CharField(max_length=60)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    author = models.ForeignKey(User, models.CASCADE)
    n_viewed = models.IntegerField(default=0, verbose_name='浏览量')
    n_commented = models.IntegerField(default=0, verbose_name='评论量')
    pass

class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    content = models.TextField(verbose_name='评论内容')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='关联帖子')
    pass
