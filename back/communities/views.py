from django.shortcuts import render
# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Subquery, OuterRef, Count, Sum, F, Prefetch
from accounts.models import User, RecommendedMovie
from movies.models import Movie
from communities.models import Article 

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import ArticleListSerializer, ArticleSerializer, CommentSerializer, RankingSerializer
from .models import Article, Comment


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def article_list(request):
    if request.method == 'GET':
        # 댓글 수 포함하여 모든 게시글 가져오기
        articles = Article.objects.annotate(comment_count=Count('comments')).select_related('movie').all()
        serializer = ArticleListSerializer(articles, many=True, context={'request': request})
        # print(serializer.data)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            article = serializer.save(user=request.user)
            user = request.user
            user.points += 10  # 100 포인트 추가
            user.save()  # 사용자 정보 저장
            # print(serializer.data)
            article_data = ArticleSerializer(article, context={'request': request}).data
            user_data = {"username": user.username, "points": user.points}
            return Response({
                "article": article_data,
                "user": user_data
            }, status=status.HTTP_201_CREATED)

        

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def article_detail(request, article_pk):
    article = get_object_or_404(Article.objects.annotate(comment_count=Count('comments')), pk=article_pk)

    if request.method == 'GET':
        serializer = ArticleListSerializer(article, context={'request': request})
        # print(serializer.data)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # 요청자가 작성자인지 확인
        if request.user != article.user:
            return Response({"error": "본인의 게시글만 수정할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
        
        # 수정 처리
        serializer = ArticleSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def delete_article(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    
    
    # 요청한 사용자가 게시글 작성자인지 확인
    if request.user != article.user:
        return Response({"error": "본인의 게시글만 삭제할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
    
    article.delete()  # 게시글 삭제
    return Response({"message": "게시글이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_article(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    user = request.user

    if user in article.like_users.all():
        article.like_users.remove(user)  # 이미 좋아요한 경우 취소
        action = 'removed'
    else:
        article.like_users.add(user)  # 좋아요 추가
        action = 'added'

    article.save()
    return Response({
        'like_count': article.like_count(),
        'action': action
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)  # 게시글을 찾음

    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, article=article)  # 현재 사용자와 게시글을 연결하여 저장
            article.refresh_from_db()
            return Response({
            "comment": serializer.data,
            "comment_count": article.comments.count()  # 최신 댓글 수 반환
        }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def get_comments(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)  # 게시글을 찾음
    comments = article.comments.all()  # 해당 게시글에 대한 댓글 가져오기
    serializer = CommentSerializer(comments, many=True)  # 댓글 목록 직렬화
    return Response(serializer.data)  # 댓글 목록 반환

def get_rank_title(points):
    """
    포인트 기준으로 랭크 타이틀 반환
    """
    if points < 1000:
        return "Bronze"
    elif points < 2000:
        return "Silver"
    elif points < 3000:
        return "Gold"
    elif points < 4000:
        return "Platinum"
    else:
        return "Diamond"

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_ranking(request):
    """
    사용자 랭킹 데이터를 반환
    """
    users = User.objects.order_by('-points')[:10]  # 상위 10명의 유저 가져오기


    ranking_data = []
    for user in users:

        rank_title = get_rank_title(user.points)  # 랭크 계산
        profile_image_url = (
            user.profile_picture.url
            if user.profile_picture
            else '/media/profile_pictures/default-profile.png'  # 디폴트 이미지 URL
        )

        likes_count = user.sum_likes  # User 모델의 sum_likes 속성을 사용

         # 추천 영화 데이터 가져오기
        recommended_movie_data = None
        if hasattr(user, 'recommended_movie'):
            recommended_movie_data = {
                "movie": {
                    "id": user.recommended_movie.movie.id,
                    "title": user.recommended_movie.movie.title,
                    "poster_url": user.recommended_movie.movie.poster_url if user.recommended_movie.movie.poster_url else '/media/default_movie_poster.png',
                },
                "reason": user.recommended_movie.reason or '추천 이유가 없습니다.',
            }

        ranking_data.append({
            "id": user.id,
            "username": user.username,
            "points": user.points,
            "rank_title": rank_title,
            "articles_count": user.articles.count(),  # 작성한 게시글 수
            "likes_count": likes_count,  # 총 좋아요 수 (sum_likes 사용)
            "followers_count": user.followers.count(),  # 팔로워 수
            "profile_picture": profile_image_url,  # 프로필 사진 URL 추가
            "recommended_movie": recommended_movie_data,
        })
        print(ranking_data)
    return Response(ranking_data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_comment(request, article_pk, comment_pk):
    """
    댓글 수정 뷰. 작성자만 수정 가능.
    """
    comment = get_object_or_404(Comment, pk=comment_pk, article_id=article_pk)
    if comment.user != request.user:
        return Response({"error": "본인의 댓글만 수정할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = CommentSerializer(comment, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, article_pk, comment_pk):
    """
    댓글 삭제 뷰. 작성자만 삭제 가능.
    """
    comment = get_object_or_404(Comment, pk=comment_pk, article_id=article_pk)
    if comment.user != request.user:
        return Response({"error": "본인의 댓글만 삭제할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
    
    comment.delete()
    return Response({"message": "댓글이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def top_reviews(request):
    """
    좋아요 순으로 상위 3개의 리뷰 반환
    """
    top_reviews = (
        Article.objects.annotate(like_count=Count('like_users'))
        .select_related('movie')
        .order_by('-like_count')[:3]
    )
    serializer = ArticleListSerializer(top_reviews, many=True, context={'request': request})
    # print(serializer.data)
    return Response(serializer.data)


