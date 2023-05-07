from django.contrib import admin
from .models import MonAn, LoaiMonAn, CuaHang, CommentMonAn, CommentCuaHang
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MonAnForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = MonAn
        fields = '__all__'


class LoaiMonAnAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description"]


class MonAnAdmin(admin.ModelAdmin):
    form = MonAnForm
    list_display = ["id", "name", "price", "created_date", "updated_date", "active"]


admin.site.register(MonAn, MonAnAdmin)
admin.site.register(LoaiMonAn)
admin.site.register(CuaHang)
admin.site.register(CommentMonAn)
admin.site.register(CommentCuaHang)
