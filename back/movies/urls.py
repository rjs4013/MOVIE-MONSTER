from django.urls import path
from . import views

urlpatterns = [
    path('', views.MovieListView.as_view(), name='movie_list'),  # 모든 영화 리스트
    path('<int:movie_id>/', views.MovieDetailView.as_view(), name='movie_detail'),  # 특정 영화 상세
    # path('genre/<str:genre_name>/', views.MoviesByGenreView.as_view(), name='movies_by_genre'),  # 장르별 영화
    path('genres/', views.GenreListView.as_view(), name='genre_list'),
    path('search/', views.search_movie, name='search-movie'), # 리뷰 쓰러 갈 때 영화 검색
]