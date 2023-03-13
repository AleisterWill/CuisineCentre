from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to='user_avatar', null=True)


class Image(models.Model):
    path = models.ImageField(upload_to='images', null=True)


class TimedModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MonAn(TimedModel):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    loaimonan = models.ForeignKey('LoaiMonAn', on_delete=models.PROTECT, null=True)
    rating_set = models.ManyToManyField('RatingMonAn', related_name="rating_set", editable=False)
    image_set = models.ManyToManyField(Image, related_name="image_set_ma")

    def __str__(self):
        return self.name


class LoaiMonAn(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name


class CuaHang(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)

    menu_set = models.ManyToManyField('Menu', related_name="menu_set", editable=False)
    rating_set = models.ManyToManyField('RatingCuaHang', related_name="rating_set", editable=False)
    image_set = models.ManyToManyField(Image, related_name="image_set_ch")

    def __str__(self):
        return self.name


class Menu(TimedModel):
    buoi = models.CharField(max_length=50)
    monan_set = models.ManyToManyField(MonAn, related_name="monan_set")

    def __str__(self):
        return self.buoi


class RatingMonAn(TimedModel):
    score = models.IntegerField()
    comment = models.TextField()

    user = models.ForeignKey(User, on_delete=models.PROTECT)


class RatingCuaHang(TimedModel):
    score = models.IntegerField()
    comment = models.TextField()

    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)








