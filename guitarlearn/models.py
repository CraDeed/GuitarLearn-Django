from django.conf import settings
from django.db import models
from django.urls import reverse



# class TimeStampedModel(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         abstract = True


class YoutubeTutorial(models.Model):
    title = models.TextField(max_length=200)
    link = models.TextField(max_length=100)
    youtuber = models.TextField(max_length=20)
    thumbnail = models.TextField(max_length=50)
    key = models.TextField(max_length=30)
    # like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.title

class PlayList(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='user_playlist', on_delete=models.CASCADE)
    title = models.TextField(blank=True,max_length=200)
    youtuber = models.TextField(blank=True,max_length=20)
    thumbnail = models.TextField(blank=True,max_length=50)
    key = models.TextField(blank=True,max_length=30)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("guitarlearn:video_detail", args=[self.pk])
