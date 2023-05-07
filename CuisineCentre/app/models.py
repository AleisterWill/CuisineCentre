from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField


class User(AbstractUser):
    avatar = models.ImageField(upload_to='user_avatar', null=True)
    is_store_owner = models.BooleanField(default=False)
    activated = models.BooleanField(default=True)


class TimedModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MonAn(TimedModel):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='monan_image/%Y/%m', null=True)
    short_description = models.TextField(null=True)
    description = RichTextField(null=True)

    cuahang = models.ForeignKey('CuaHang', on_delete=models.CASCADE, null=True)
    loaimonan = models.ForeignKey('LoaiMonAn', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name


class LoaiMonAn(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True)


class CuaHang(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    image = models.ImageField(upload_to='cuahang_image/%Y/%m', null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class MonAnActionAbstract(TimedModel):
    monan = models.ForeignKey(MonAn, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('monan', 'user')
        abstract = True


class LikeMonAn(MonAnActionAbstract):
    liked = models.BooleanField(default=True)


class RatingMonAn(MonAnActionAbstract):
    rate = models.FloatField(default=0)


class CommentMonAn(TimedModel):
    noi_dung = models.TextField()

    monan = models.ForeignKey(MonAn, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class CuaHangActionAbstract(TimedModel):
    cuahang = models.ForeignKey(CuaHang, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('cuahang', 'user')
        abstract = True


class LikeCuaHang(CuaHangActionAbstract):
    liked = models.BooleanField(default=True)


class RatingCuaHang(CuaHangActionAbstract):
    rate = models.FloatField(default=0)


class CommentCuaHang(TimedModel):
    noi_dung = models.TextField()

    cuahang = models.ForeignKey(CuaHang, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class DonHang(TimedModel):
    monan = models.ForeignKey(MonAn, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)
    total = models.IntegerField(default=0)
    status = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class HoaDon(TimedModel):
    status = models.CharField(max_length=50)
    total = models.IntegerField(default=0)

    donhang = models.ForeignKey(DonHang, on_delete=models.CASCADE)







