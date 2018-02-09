from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Photo(models.Model):
    image = models.FileField()
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    @property
    def quantity_of_likes(self):
        return self.like_set.filter(liked=True).count()

    @property
    def quantity_of_dislikes(self):
        return self.like_set.filter(liked=False).count()

    def __str__(self):
        return "Photo ID: {}".format(str(self.id))


class Like(models.Model):
    liked = models.BooleanField(default=False)
    author = models.ForeignKey(User)
    photo = models.ForeignKey(Photo)


class Comment(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    photo = models.ForeignKey(Photo)

    def __str__(self):
        return self.content

