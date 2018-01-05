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


class Like(models.Model):
    liked = models.BooleanField(default=False)
    author = models.ForeignKey(User)
    photo = models.ForeignKey(Photo)

