from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('MonAn', views.MonAnViewSet)
router.register('LoaiMonAn', views.LoaiMonAnViewSet)
router.register('CommentMonAn', views.CommentMonAnViewSet)
router.register('CuaHang', views.CuaHangViewSet)
router.register('CommentCuaHang', views.CommentCuaHangViewSet)
router.register('User', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls))
]
