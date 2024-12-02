from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models import Count
from movies.models import Movie  # Movie 모델 참조
from PIL import Image  # Pillow 라이브러리
import os

class User(AbstractUser):
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True,
        # default='profile_pictures/default-profile.png'  # 기본 이미지 경로 설정
    )
    points = models.IntegerField(default=500)
    followings = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def sum_likes(self):
        """
        사용자가 작성한 게시글에 대한 총 좋아요 수를 반환
        """
        from communities.models import Article  # 순환 참조 방지
        return Article.objects.filter(user=self).aggregate(total_likes=Count('like_users'))['total_likes'] or 0
    
    # 이미지 크기 조정
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # 먼저 모델 저장

        if self.profile_picture:
            image_path = self.profile_picture.path
            with Image.open(image_path) as img:
                img.thumbnail((300, 300))  # 원하는 크기로 조정 (예: 300x300)
                img.save(image_path)  # 이미지 저장
        
        default_image_path = os.path.join('media', 'profile_pictures', 'default-profile.png')
        if os.path.exists(default_image_path):
            with Image.open(default_image_path) as default_img:
                default_img.thumbnail((300, 300))
                default_img.save(default_image_path)
    
    def get_profile_picture_url(self):
        if self.profile_picture:
            return self.profile_picture.url
        return '/media/profile_pictures/default-profile.png' # 기본 이미지

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=30)
    movies = models.ManyToManyField(Movie, related_name='categories')  # ManyToMany 관계 추가
    def __str__(self):
        return self.name
    
class CategoryMovie(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_movies')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_categories')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category.name} - {self.movie.title}"

class Ranking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rankings')
    rank = models.IntegerField()
    week_start = models.DateField()
    week_end = models.DateField()

class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games')
    game_type = models.CharField(max_length=50)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class RecommendedMovie(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recommended_movie')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='recommended_by')
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s recommendation: {self.movie.title}"

