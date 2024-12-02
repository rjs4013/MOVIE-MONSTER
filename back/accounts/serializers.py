from rest_framework import serializers
from .models import User, Category, Ranking, Game, RecommendedMovie
from movies.models import Movie
from dj_rest_auth.registration.serializers import RegisterSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'profile_picture',
            'points',
            'follower',
            'following',
            'created_at',
        ]

class CustomRegisterSerializer(RegisterSerializer):
    profile_picture = serializers.ImageField(required=False)  # 프로필 사진 필드 추가

    def custom_signup(self, request, user):
        profile_picture = self.validated_data.get('profile_picture')
        print("DEBUG: Profile Picture -", profile_picture)
        if profile_picture:
            user.profile_picture = profile_picture
            print(user.profile_picture)  # 저장된 경로 출력
            user.save()


class ProfileSerializer(serializers.ModelSerializer):
    articles_count = serializers.IntegerField(source='articles.count', read_only=True)  # 게시글 수
    likes_count = serializers.IntegerField(source='sum_likes', read_only=True)  # 총 좋아요 수

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'points',
            'follower',
            'following',
            'articles_count',
            'likes_count',  # sum_likes 매핑
        ]

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'poster_url', 'release_date']
        
class CategorySerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'movies']


class RankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ranking
        fields = ['id', 'user', 'rank', 'week_start', 'week_end']

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'user', 'game_type', 'score', 'created_at']

class UserRankSerializer(serializers.ModelSerializer):
    rank_title = serializers.SerializerMethodField()

    def get_rank_title(self, obj):
        print(f"User: {obj.username}, Points: {obj.points}")  # 디버깅용 로그
        if obj.points < 1000:
            return "Bronze"
        elif obj.points < 2000:
            return "Silver"
        elif obj.points < 3000:
            return "Gold"
        elif obj.points < 4000:
            return "Platinum"
        else:
            return "Diamond"

    class Meta:
        model = User
        fields = ['username', 'points', 'rank_title', 'articles_count', 'likes_count', 'followers_count']

class RecommendedMovieSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()  # Nested serializer to include movie details

    class Meta:
        model = RecommendedMovie
        fields = ['id', 'movie', 'reason']

class RecommendedMovieCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendedMovie
        fields = ['movie', 'reason']

