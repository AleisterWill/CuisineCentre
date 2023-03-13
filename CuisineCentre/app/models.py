from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to='user_avatar', null=True)


class TimedModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MonAn(TimedModel):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    loaimonan = models.ForeignKey('LoaiMonAn', on_delete=models.PROTECT, default=None)

    def __str__(self):
        return self.name


class LoaiMonAn(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name






