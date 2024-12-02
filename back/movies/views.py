import os
import json
from django.http import JsonResponse
from django.views import View
from .models import Movie, Genre
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings  # BASE_DIR 사용

# 모든 영화 조회
class MovieListView(View):
    def get(self, request):
        movies = Movie.objects.all().values('id', 'title', 'poster_url', 'backdrop_url')  # backdrop_url 추가
        return JsonResponse(list(movies), safe=False)

# JSON 파일 경로 설정
JSON_FILE_PATH = os.path.join(settings.BASE_DIR, "movies", "fixtures", "movies", "movie_data.json")

class MovieDetailView(View):
    def get(self, request, movie_id):
        try:
            # JSON 파일 열기
            with open(JSON_FILE_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)

            # 요청된 movie_id에 해당하는 영화 검색
            for entry in data:
                fields = entry["fields"]
                if fields["movie_id"] == movie_id:
                    # 영화 데이터 구성
                    movie = {
                        "id": fields["movie_id"],
                        "title": fields["title"],
                        "poster_url": fields["poster_url"],
                        "backdrop_url": fields.get("backdrop_url", None),  # backdrop_url 추가
                        "vote_avg": fields["vote_avg"],
                        "director": fields["director"],
                        "release_date": fields["release_date"],
                        "description": fields["description"],
                        "genres": fields["genres"],  # 리스트 그대로 반환
                        "actors": fields["actors"],  # 리스트 그대로 반환
                    }
                    return JsonResponse(movie)

            # 해당 movie_id를 찾을 수 없는 경우
            return JsonResponse({"error": "Movie not found"}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

class GenreListView(View):
    def get(self, request):
        genres = Genre.objects.all().values('id', 'name')  # id와 name만 반환
        return JsonResponse(list(genres), safe=False)

from django.db.models import Q

@api_view(['GET'])
def search_movie(request):
    movie_title = request.query_params.get('title', None)

    if not movie_title:
        return Response({"error": "영화 제목을 입력해 주세요."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # 공백 없는 제목을 공백으로 분리
        title_query = movie_title.replace(" ", "")
        movies = Movie.objects.filter(
            title__icontains=title_query  # 부분 매칭 수행
        ) | Movie.objects.filter(
            title__iregex=r"".join(f"{char}.*" for char in title_query)  # 각 글자를 순차 매칭
        )

        if movies.exists():
            results = [
                {
                    "id": movie.id,
                    "title": movie.title,
                    "poster_url": movie.poster_url,
                    "backdrop_url": movie.backdrop_url,  # backdrop_url 추가
                    "description": movie.description,
                }
                for movie in movies
            ]
            return Response(results)
        else:
            return Response({"error": "영화가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
