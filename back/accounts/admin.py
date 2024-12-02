from django.contrib import admin
from .models import User, Category, Ranking, Game

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Ranking)
admin.site.register(Game)
