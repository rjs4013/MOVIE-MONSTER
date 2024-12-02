from django.db import models
from django.conf import settings
from movies.models import Movie


class Article(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles'
    )
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='like_articles'
    )
    title = models.CharField(max_length=100)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True, related_name="articles")  # Movie 모델 연결
    content = models.TextField()
    rating = models.IntegerField(default=0)  # 소수점 대신 정수형으로 변경
    poster_url = models.URLField(max_length=500, blank=True, null=True)  # 포스터 URL 필드 추가
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def like_count(self):
        return self.like_users.count()

class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)  # 특정 게시글에 연결
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 댓글 작성자
    content = models.TextField()  # 댓글 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 댓글 작성 시간