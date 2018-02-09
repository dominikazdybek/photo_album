from django.contrib import admin
from .models import Photo, Like, Comment

# Register your models here.


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("image", "creation_date", "user")


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("liked", "author", "photo")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("content", "date", "author", "photo")
