from rest_framework import serializers
from .models import MonAn, LoaiMonAn, CommentMonAn, CuaHang, CommentCuaHang, User, DonHang, HoaDon
from django.db.models import Avg


class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='avatar')

    def get_image(self, user):
        if user.avatar:
            request = self.context.get('request')
            return request.build_absolute_uri('/static/%s' % user.avatar.name) if request else ''

    def create(self, validated_data):
        data = validated_data.copy()
        print(data)
        u = User(**data)
        u.set_password(u.password)
        u.save()
        return u

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password', 'avatar', 'image', 'is_store_owner',
                  'activated']
        extra_kwargs = {
            'password': {'write_only': True},
            'avatar': {'write_only': True},
        }


class LoaiMonAnSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoaiMonAn
        fields = ['id', 'name']


class CommentMonAnSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = CommentMonAn
        fields = ['id', 'created_date', 'noi_dung', 'user']


class CuaHangSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')
    rate_average = serializers.SerializerMethodField()

    def get_image(self, CuaHang):
        if CuaHang.image:
            request = self.context.get('request')
            return request.build_absolute_uri('/static/%s' % CuaHang.image.name) if request else ''

    def get_rate_average(self, cuahang):
        return cuahang.ratingcuahang_set.aggregate(Avg('rate'))

    class Meta:
        model = CuaHang
        fields = ['id', 'name', 'address', 'image', 'rate_average', 'user']


class AuthorizedCuaHangSerializer(CuaHangSerializer):
    liked = serializers.SerializerMethodField()
    liked_count = serializers.SerializerMethodField()
    rate = serializers.SerializerMethodField()

    def get_liked(self, cuahang):
        request = self.context.get('request')
        if request:
            return cuahang.likecuahang_set.filter(user=request.user, liked=True).exists()

    def get_liked_count(self, cuahang):
        return cuahang.likecuahang_set.count()

    def get_rate(self, cuahang):
        request = self.context.get('request')
        if request:
            r = cuahang.ratingcuahang_set.filter(user=request.user).first()
            return r.rate if r else 0

    class Meta:
        model = CuaHangSerializer.Meta.model
        fields = CuaHangSerializer.Meta.fields + ['liked', 'liked_count', 'rate', ]


class CommentCuaHangSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = CommentCuaHang
        fields = ['id', 'created_date', 'noi_dung', 'user', ]


class MonAnSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')
    cuahang = CuaHangSerializer()
    loaimonan = LoaiMonAnSerializer()
    rate_average = serializers.SerializerMethodField()

    def get_image(self, MonAn):
        if MonAn.image:
            request = self.context.get('request')
            return request.build_absolute_uri('/static/%s' % MonAn.image.name) if request else ''

    def get_rate_average(self, monan):
        return monan.ratingmonan_set.aggregate(Avg('rate'))

    class Meta:
        model = MonAn
        fields = ['id', 'name', 'price', 'loaimonan', 'short_description', 'description', 'image', 'cuahang',
                  'rate_average']


class AuthorizedMonAnSerializer(MonAnSerializer):
    liked = serializers.SerializerMethodField()
    liked_count = serializers.SerializerMethodField()
    rate = serializers.SerializerMethodField()

    def get_liked(self, monan):
        request = self.context.get('request')
        if request:
            return monan.likemonan_set.filter(user=request.user, liked=True).exists()

    def get_liked_count(self, monan):
        return monan.likemonan_set.filter(liked=True).count()

    def get_rate(self, monan):
        request = self.context.get('request')
        if request:
            r = monan.ratingmonan_set.filter(user=request.user).first()
            return r.rate if r else 0

    class Meta:
        model = MonAnSerializer.Meta.model
        fields = MonAnSerializer.Meta.fields + ['liked', 'liked_count', 'rate']


class DonHangSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonHang
        fields = ['id', 'created_date', 'updated_date', 'monan', 'price', 'quantity', 'total', 'status', 'user']


class HoaDonSerializer(serializers.ModelSerializer):
    class Meta:
        model = HoaDon
        fields = ['id', 'created_date', 'updated_date', 'status', 'total', 'donhang']
