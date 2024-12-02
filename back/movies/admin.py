from django.contrib import admin
from .models import Movie, Genre, Actor

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date')  # 'genres'는 다대다 관계로 표시가 어려우므로 제거
    search_fields = ('title',)
    list_filter = ('release_date',)

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Actor)