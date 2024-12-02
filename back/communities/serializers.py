from rest_framework import serializers
from .models import Article, Comment
from movies.models import Movie  # Movie 모델 가져오기
from accounts.models import User  # 사용자 모델 가져오기


class MovieSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()  # genres 필드를 직접 변환

    class Meta:
        model = Movie
        fields = ('movie_id', 'title', 'poster_url', 'genres', 'description', 'vote_avg')

    def get_genres(self, obj):
        # genres가 쉼표로 구분된 문자열로 저장되어 있다면 이를 배열로 분할
        if obj.genres:
            return obj.genres.strip("[]").replace("'", "").split(', ')
        return []  # 만약 데이터가 없다면 빈 배열 반환





class ArticleListSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    user = serializers.StringRelatedField()
    movie = MovieSerializer()  # 영화 관련 필드를 가져오기 위해 Nested Serializer 사용
    user_profile_image = serializers.SerializerMethodField()  # 사용자 프로필 이미지 추가
    is_liked = serializers.SerializerMethodField()  # 좋아요 상태 추가

    def get_is_liked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return user in obj.like_users.all()  # 현재 사용자가 좋아요한 상태 반환
        return False

    class Meta:
        model = Article
        fields = (
            'id', 'title', 'content', 'like_count', 'comment_count',
            'user', 'user_profile_image', 'rating', 'created_at', 'updated_at',
            'is_liked', 'movie'
        )
    
    def get_user_profile_image(self, obj):
        user = obj.user
        if hasattr(user, 'get_profile_picture_url'):
            return user.get_profile_picture_url()
        return '/media/profile_pictures/default-profile.png'  # 기본값


class ArticleSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True)
    user = serializers.StringRelatedField()
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())
    is_liked = serializers.SerializerMethodField()  # 좋아요 상태 추가
    comment_count = serializers.IntegerField(read_only=True)

    def get_is_liked(self, obj):
        request = self.context.get('request', None)
        if not request or not hasattr(request, 'user') or request.user.is_anonymous:
            return False  # 요청이 없거나 인증되지 않은 경우 False 반환
        return request.user in obj.like_users.all()

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user', 'like_users', 'comment_count')


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # 댓글 작성자 이름을 문자열로 반환

    class Meta:
        model = Comment
        fields = ('id', 'user', 'content', 'created_at')  # 댓글 ID, 작성자, 내용, 작성시간 반환


class RankingSerializer(serializers.ModelSerializer):
    articles_count = serializers.IntegerField()  # 게시물 수
    likes_count = serializers.IntegerField()  # 좋아요 수
    followers_count = serializers.IntegerField()  # 팔로워 수

    class Meta:
        model = User
        fields = ('id', 'username', 'points', 'articles_count', 'likes_count', 'followers_count')
