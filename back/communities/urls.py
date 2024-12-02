from django.urls import path
from . import views


urlpatterns = [
    path('', views.article_list),
    path('<int:article_pk>/', views.article_detail),
    path('<int:article_pk>/like/', views.like_article, name='like-article'),
    path('<int:article_pk>/comments/', views.create_comment, name='create-comment'),
    path('<int:article_pk>/comments/list/', views.get_comments, name='get-comments'),  # 댓글 목록 요청 추가
    path('<int:article_pk>/comments/<int:comment_pk>/update/', views.update_comment, name='update-comment'),  # 댓글 수정
    path('<int:article_pk>/comments/<int:comment_pk>/delete/', views.delete_comment, name='delete-comment'),  # 댓글 삭제
    path('<int:article_pk>/delete/', views.delete_article, name='delete_article'),  # 삭제 엔드포인트 추가
    path('ranking/', views.get_ranking, name='get_ranking'),
    path('top-reviews/', views.top_reviews, name='top-reviews'),
]