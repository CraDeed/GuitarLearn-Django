from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import resolve_url

class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = "M", "남성"
        FEMALE = "F", "여성"
        ETC = "ETC", "기타"

    email = models.EmailField(unique=True)
    avatar = models.ImageField(
        blank=True, upload_to="accounts/avatar/%Y/%m/%d",
        help_text="48px * 48px 크기의 png/jpg 파일을 업로드해주세요")

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return resolve_url('/static/avatar.png')