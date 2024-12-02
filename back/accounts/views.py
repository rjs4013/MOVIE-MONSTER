from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db.models import Count
from .models import User, Category, Ranking, Game, RecommendedMovie
from .serializers import UserSerializer, CategorySerializer, MovieSerializer, RankingSerializer, GameSerializer, ProfileSerializer, UserRankSerializer, RecommendedMovieSerializer, RecommendedMovieCreateSerializer
from movies.models import Movie
from django.middleware.csrf import get_token

from dj_rest_auth.registration.views import RegisterView
from .serializers import CustomRegisterSerializer, MovieSerializer
from rest_framework.parsers import MultiPartParser, FormParser

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer
    parser_classes = [MultiPartParser, FormParser]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_category(request):
    user = request.user
    name = request.data.get('name')

    if not name or not name.strip():
        return Response({'error': 'Category name cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)

    if Category.objects.filter(user=user, name=name).exists():
        return Response({'error': 'Category with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        category = Category.objects.create(user=user, name=name.strip())
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': f'Failed to create category: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_categories(request):
    user = request.user
    categories = Category.objects.filter(user=user)
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

from movies.models import Movie
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_movie_to_category(request):
    user = request.user
    category_id = request.data.get('category_id')
    movie_id = request.data.get('movie_id')

    if not category_id or not movie_id:
        return Response(
            {'error': 'category_id와 movie_id는 필수 항목입니다.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        category = Category.objects.get(id=category_id, user=user)
    except Category.DoesNotExist:
        return Response(
            {'error': '해당 카테고리를 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        movie = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return Response(
            {'error': '해당 영화를 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND,
        )

    # ManyToManyField 또는 Custom 관계 추가
    category.movies.add(movie)

    return Response(
        {'message': f'영화 "{movie.title}"가 카테고리 "{category.name}"에 추가되었습니다.'},
        status=status.HTTP_200_OK,
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_detail(request, category_id):
    """
    특정 카테고리의 상세 정보 및 연결된 영화 반환
    """
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response({'error': '해당 카테고리를 찾을 수 없습니다.'}, status=404)

    movies = category.movies.all()
    movie_serializer = MovieSerializer(movies, many=True)
    return Response({
        'id': category.id,
        'name': category.name,
        'owner_id': category.user.id,  # 소유자 ID
        'movies': movie_serializer.data,  # 영화 데이터 포함
    }, status=200)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_category_name(request, category_id):
    """
    카테고리 이름 수정
    """
    try:
        category = Category.objects.get(id=category_id, user=request.user)
        print(f"Category belongs to: {category.user.id}, Request user: {request.user.id}")
    except Category.DoesNotExist:
        return Response({'error': '해당 카테고리를 찾을 수 없습니다.'}, status=404)

    new_name = request.data.get('name', '').strip()
    if not new_name:
        return Response({'error': '새 이름을 입력해야 합니다.'}, status=400)

    category.name = new_name
    category.save()
    return Response({'message': '카테고리 이름이 수정되었습니다.', 'name': category.name}, status=200)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_category(request, category_id):
    """
    사용자의 카테고리 삭제
    """
    try:
        category = Category.objects.get(id=category_id, user=request.user)
        category.delete()
        return Response({'message': '카테고리가 삭제되었습니다.'}, status=200)
    except Category.DoesNotExist:
        return Response({'error': '해당 카테고리를 찾을 수 없습니다.'}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_movie_from_category(request):
    """
    카테고리에서 특정 영화 삭제
    """
    category_id = request.data.get('category_id')
    movie_id = request.data.get('movie_id')

    if not category_id or not movie_id:
        return Response({'error': 'category_id와 movie_id는 필수 항목입니다.'}, status=400)

    try:
        category = Category.objects.get(id=category_id, user=request.user)
        movie = Movie.objects.get(id=movie_id)
        category.movies.remove(movie)
        return Response({'message': f'영화 "{movie.title}"가 카테고리 "{category.name}"에서 삭제되었습니다.'}, status=200)
    except Category.DoesNotExist:
        return Response({'error': '해당 카테고리를 찾을 수 없습니다.'}, status=404)
    except Movie.DoesNotExist:
        return Response({'error': '해당 영화를 찾을 수 없습니다.'}, status=404)
    

# 사용자 프로필 정보 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

# 사용자 목록 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST', 'GET'])  # POST와 GET 모두 지원
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def user_points(request):
    user = request.user  # 현재 로그인한 유저

    if request.method == 'POST':
        # 프론트에서 받은 추가 점수 처리
        points_to_add = request.data.get('points', 0)
        user.points += points_to_add
        user.save()
        return Response(
            {
                'message': 'Points updated successfully!',
                'username': user.username,
                'current_points': user.points
            },
            status=status.HTTP_200_OK
        )

    elif request.method == 'GET':
        # 유저 정보 반환
        return Response(
            {
                'username': user.username,
                'current_points': user.points
            },
            status=status.HTTP_200_OK
        )
        
from communities.models import Article  # Article 모델 임포트

from django.db.models import Count

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def profile(request, username):
#     """
#     사용자 프로필 데이터를 반환하며,
#     각 카테고리의 첫 번째 영화 포스터를 포함합니다.
#     """
#     user = get_object_or_404(User, username=username)

#     # 사용자 카테고리 데이터
#     categories = Category.objects.filter(user=user)
#     category_data = []
#     for category in categories:
#         # 카테고리에서 첫 번째 영화 가져오기
#         first_movie = category.movies.first()  # ManyToMany 관계
#         category_data.append({
#             'id': category.id,
#             'name': category.name,
#             'movies_count': category.movies.count(),  # 영화 개수
#             'first_movie_poster': first_movie.poster_url if first_movie else '/media/default_categories/default-category.png',  # 첫 번째 영화 포스터 또는 디폴트 이미지
#         })

#     # 게시글 및 좋아요 데이터
#     articles_count = Article.objects.filter(user=user).count()
#     likes_count = Article.objects.filter(user=user).aggregate(
#         total_likes=Count('like_users')
#     )['total_likes'] or 0

#     # 응답 데이터
#     return Response({
#         'id': user.id,
#         'username': user.username,
#         'points': user.points,
#         'followers_count': user.followers.count(),
#         'followings_count': user.followings.count(),
#         'articles_count': articles_count,
#         'likes_count': likes_count,
#         'is_followed': request.user in user.followers.all(),
#         'categories': category_data,
#         'profile_image': user.profile_picture.url if user.profile_picture else '/media/profile_pictures/default-profile.png',
#     })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request, username):
    # 사용자 객체 가져오기
    user = get_object_or_404(User, username=username)

    # 해당 유저의 카테고리 가져오기
    categories = Category.objects.filter(user=user)
    category_data = []
    for category in categories:
        # 카테고리에서 첫 번째 영화 가져오기
        first_movie = category.movies.first()  # ManyToMany 관계
        category_data.append({
            'id': category.id,
            'name': category.name,
            'movies_count': category.movies.count(),  # 영화 개수
            'first_movie_poster': first_movie.poster_url if first_movie else '/media/default_categories/default-category.png',  # 첫 번째 영화 포스터 또는 디폴트 이미지
        })
    category_serializer = CategorySerializer(categories, many=True)

    # 게시글 수와 좋아요 수 계산
    articles_count = Article.objects.filter(user=user).count()
    likes_count = Article.objects.filter(user=user).aggregate(
        total_likes=Count('like_users')
    )['total_likes'] or 0

    # 추천 영화 데이터 가져오기
    try:
        recommended_movie = RecommendedMovie.objects.get(user=user)
        movie_data = recommended_movie.movie
        recommended_movie_data = {
            'movie': {
                'id': movie_data.id,
                'title': movie_data.title,
                'poster_url': movie_data.poster_url if movie_data.poster_url else '/media/default_movie_poster.png',  # 기본 이미지 제공
            },
            'reason': recommended_movie.reason or '추천 이유가 없습니다.',
        }
    except RecommendedMovie.DoesNotExist:
        recommended_movie_data = None


    return Response({
        'id': user.id,
        'username': user.username,
        'points': user.points,  # 포인트
        'followers_count': user.followers.count(),  # 팔로워 수
        'followings_count': user.followings.count(),  # 팔로잉 수
        'articles_count': articles_count,  # 작성한 게시글 수
        'likes_count': likes_count,  # 총 좋아요 수
        'is_followed': request.user in user.followers.all(),  # 현재 사용자가 팔로우 중인지 여부
        'categories': category_serializer.data,  # 유저 카테고리 포함
        'profile_image': user.profile_picture.url if user.profile_picture else '/media/profile_pictures/default-profile.png',
        'recommended_movie': recommended_movie_data,  # 추천 영화 데이터 포함
        'category_image': category_data,
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request, user_pk):
    User = get_user_model()
    person = User.objects.get(pk=user_pk)
    user = request.user
    if person != user:
        if person.followers.filter(pk=user.pk).exists():
            person.followers.remove(user)
            is_followed = False
        else:
            person.followers.add(user)
            is_followed = True
        context = {
            'is_followed': is_followed,
            'followings_count': person.followings.count(),
            'followers_count': person.followers.count(),
        }
        return JsonResponse(context)
    return redirect('accounts:profile', person.username)


from django.middleware.csrf import get_token

@api_view(['GET'])
def get_csrf_token(request):
    csrf_token = get_token(request)
    return Response({'csrfToken': csrf_token})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_movies(request):
    """
    영화 제목으로 검색
    """
    title = request.query_params.get('title', '').strip()
    if not title:
        return Response({'error': '영화 제목을 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

    movies = Movie.objects.filter(title__icontains=title)[:10]  # 제목에 검색어가 포함된 영화 10개 제한
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_movie_to_category(request):
    """
    카테고리에 영화 추가
    """
    category_id = request.data.get('category_id')
    movie_id = request.data.get('movie_id')

    if not category_id or not movie_id:
        return Response({'error': 'category_id와 movie_id는 필수 항목입니다.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        category = Category.objects.get(id=category_id, user=request.user)
        movie = Movie.objects.get(id=movie_id)
    except Category.DoesNotExist:
        return Response({'error': '카테고리를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
    except Movie.DoesNotExist:
        return Response({'error': '영화를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    category.movies.add(movie)
    return Response({'message': f'영화 "{movie.title}"가 카테고리 "{category.name}"에 추가되었습니다.'}, status=status.HTTP_200_OK)


## 추천 영화 기능
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def recommend_movie(request):
    user = request.user

    if request.method == 'GET':
        try:
            recommendation = RecommendedMovie.objects.get(user=user)
            serializer = RecommendedMovieSerializer(recommendation)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except RecommendedMovie.DoesNotExist:
            return Response({'detail': '추천 영화가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        movie_id = request.data.get('movie_id')  # movie_id 필드 확인
        reason = request.data.get('reason')  # reason 필드 확인

        if not movie_id or not reason:
            return Response(
                {'error': 'movie_id와 reason 필드는 필수입니다.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            movie = Movie.objects.get(id=movie_id)  # 영화 존재 여부 확인
        except Movie.DoesNotExist:
            return Response(
                {'error': '해당 영화를 찾을 수 없습니다.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # 기존 추천 수정 또는 새로운 추천 생성
        recommendation, created = RecommendedMovie.objects.update_or_create(
            user=user,
            defaults={'movie': movie, 'reason': reason}
        )

        serializer = RecommendedMovieSerializer(recommendation)
        return Response(serializer.data, status=status.HTTP_200_OK)  # 수정: 메시지 제거

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_categories(request, username):
    """
    특정 사용자의 카테고리를 반환하는 뷰
    """
    user = get_object_or_404(User, username=username)  # 유저 확인
    categories = Category.objects.filter(user=user)  # 해당 유저의 카테고리 가져오기
    serializer = CategorySerializer(categories, many=True)  # 직렬화
    return Response(serializer.data, status=200)  # 응답 반환
