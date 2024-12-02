from django.urls import path, include
from . import views
from .views import CustomRegisterView

urlpatterns = [
    # path('register/', views.register_user, name='register_user'),
    # path('login/', views.login_user, name='login_user'),
    path('', include('dj_rest_auth.urls')),  # 로그인, 로그아웃, 패스워드 변경 등
    path('custom-signup/', CustomRegisterView.as_view(), name='custom_signup'),  # 커스텀 경로
    path('signup/', include('dj_rest_auth.registration.urls')),  # 회원가입 관련 URL
    # path('profile/', views.get_user_profile, name='get_user_profile'),
    path("profile/<username>/", views.profile, name="profile"),
    path("<int:user_pk>/follow/", views.follow, name="follow"),
    path('users/', views.get_users, name='get_users'),
    path('categories/', views.get_categories, name='get_categories'),
    path('categories/create/', views.create_category, name='create_category'),
    path('categories/add-movie/', views.add_movie_to_category, name='add_movie_to_category'),
    path('categories/<int:category_id>/', views.category_detail, name='category_detail'),
    path('categories/<int:category_id>/update/', views.update_category_name, name='update_category_name'),
    path('categories/<int:category_id>/delete/', views.delete_category, name='delete_category'),
    path('categories/remove-movie/', views.remove_movie_from_category, name='remove_movie_from_category'),
    # path('rankings/', views.get_user_rankings, name='get_user_rankings'),
    # path('games/', views.manage_games, name='manage_games'),
    path('csrf-token/', views.get_csrf_token, name='get_csrf_token'),
    path('user/points/', views.user_points, name='user_points'),
    path('categories/add-movie/', views.add_movie_to_category, name='add_movie_to_category'),
    path('movies/search/', views.search_movies, name='search_movies'),
    path('recommend-movie/', views.recommend_movie, name='recommend_movie'),
    path('profile/<username>/categories/', views.get_user_categories, name='get_user_categories'),
]
