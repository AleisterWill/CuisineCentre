from django.contrib import admin
from .models import MonAn, LoaiMonAn, RatingMonAn, RatingCuaHang, Menu, CuaHang, Image


class LoaiMonAnAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description"]


class MonAnAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "price", "created_date", "updated_date", "active"]


admin.site.register(MonAn)
admin.site.register(LoaiMonAn)
admin.site.register(RatingMonAn)
admin.site.register(RatingCuaHang)
admin.site.register(Menu)
admin.site.register(CuaHang)
admin.site.register(Image)

