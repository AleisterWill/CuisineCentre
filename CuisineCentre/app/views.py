from rest_framework import viewsets, permissions, generics, parsers, status
from rest_framework.decorators import action
from rest_framework.views import Response
from django.db.models import Q
from .paginators import MonAnPaginator, CuaHangPaginator, CommentMonAnPaginator, CommentCuaHangPaginator

from .models import MonAn, LoaiMonAn, LikeMonAn, RatingMonAn, CommentMonAn, CuaHang, LikeCuaHang, RatingCuaHang, \
    CommentCuaHang, User, DonHang, HoaDon
from .serializers import MonAnSerializer, AuthorizedMonAnSerializer, LoaiMonAnSerializer, CommentMonAnSerializer, \
    CuaHangSerializer, AuthorizedCuaHangSerializer, CommentCuaHangSerializer, UserSerializer, DonHangSerializer, \
    HoaDonSerializer

from .permissions import IsStoreOwner


class MonAnViewSet(viewsets.ViewSet, generics.RetrieveAPIView, generics.ListAPIView):
    queryset = MonAn.objects.filter(active=True)
    serializer_class = MonAnSerializer
    pagination_class = MonAnPaginator

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return AuthorizedMonAnSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action in ['post_comment', 'like', 'rate', 'post_order']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def filter_queryset(self, queryset):
        q = queryset

        cuahang_id = self.request.query_params.get('cuahang_id')
        if cuahang_id:
            q = q.filter(cuahang__id=cuahang_id)

        kw = self.request.query_params.get('kw')
        if kw:
            q = q.filter(Q(name__icontains=kw) | Q(loaimonan__name__icontains=kw))

        return q.order_by('-created_date')

    @action(methods=['post'], detail=True, url_path='order')
    def post_order(self, request, pk):
        o = DonHang(
            price=request.data['price'],
            quantity=request.data['quantity'],
            total=request.data['total'],
            status=request.data['status'],
            monan=self.get_object(),
            user=request.user
        )
        o.save()
        return Response(status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, url_path='comment')
    def post_comment(self, request, pk):
        c = CommentMonAn(
            noi_dung=request.data['noi_dung'],
            user=request.user,
            monan=self.get_object()
        )
        c.save()

        return Response(CommentMonAnSerializer(c, context={'request': request}).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, url_path='like')
    def like(self, request, pk):
        l, existed = LikeMonAn.objects.get_or_create(user=request.user, monan=self.get_object())
        if not existed:
            l.liked = not l.liked
        l.save()

        return Response(AuthorizedMonAnSerializer(self.get_object(), context={"request": request}).data,
                        status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='rate')
    def rate(self, request, pk):
        r, existed = RatingMonAn.objects.get_or_create(user=request.user, monan=self.get_object())
        r.rate = request.data['rate']
        r.save()

        return Response(AuthorizedMonAnSerializer(self.get_object(), context={"request": request}).data,
                        status=status.HTTP_200_OK)


class LoaiMonAnViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.RetrieveAPIView):
    queryset = LoaiMonAn.objects.all()
    serializer_class = LoaiMonAnSerializer

    def create(self, request, *args, **kwargs):
        loai = LoaiMonAn(
            name=request.data['name'],
            description=request.data['desc']
        )
        loai.save()

        return Response(LoaiMonAnSerializer(loai, context={"request": request}).data, status=status.HTTP_201_CREATED)


class CommentMonAnViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = CommentMonAn.objects.all()
    serializer_class = CommentMonAnSerializer
    pagination_class = CommentMonAnPaginator

    def filter_queryset(self, queryset):
        q = queryset
        monan_id = self.request.query_params.get('monan_id')

        return q.filter(monan__id=monan_id).order_by('-created_date') if monan_id else []


class CuaHangViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = CuaHang.objects.all()
    serializer_class = CuaHangSerializer
    pagination_class = CuaHangPaginator

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return AuthorizedCuaHangSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action in ['post_monan', 'edit_or_del_monan']:
            return [IsStoreOwner(), ]

        if self.action in ['like', 'rate', 'comment']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['post'], detail=True, url_path='post_monan')
    def post_monan(self, request, pk):
        ma = MonAn(
            name=request.data['name'],
            price=request.data['price'],
            loaimonan=LoaiMonAn.objects.get(id=request.data['loaimonan_id']),
            image=request.data['image'],
            active=True if request.data['active'] == "true" else False,
            short_description=request.data['short_description'],
            description=request.data['description'],
            cuahang=self.get_object()
        )
        ma.save()
        return Response(MonAnSerializer(ma, context={"request": request}).data, status=status.HTTP_201_CREATED)

    @action(methods=['put', 'delete'], detail=True, url_path='monan')
    def edit_or_del_monan(self, request, pk):
        if request.method.__eq__('DELETE'):
            monan_id = request.query_params.get('monan_id')
            if monan_id:
                monan = MonAn.objects.filter(id=monan_id).delete()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        pass

    @action(methods=['post'], detail=True, url_path='like')
    def like(self, request, pk):
        l, existed = LikeCuaHang.objects.get_or_create(user=request.user, cuahang=self.get_object())
        if not existed:
            l.liked = not l.liked
        l.save()

        return Response(AuthorizedCuaHangSerializer(self.get_object(), context={"request": request}).data,
                        status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='rate')
    def rate(self, request, pk):
        r, existed = RatingCuaHang.objects.get_or_create(user=request.user, cuahang=self.get_object())
        r.rate = request.data['rate']
        r.save()

        return Response(AuthorizedCuaHangSerializer(self.get_object(), context={"request": request}).data,
                        status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='comment')
    def post_comment(self, request, pk):
        c = CommentCuaHang(
            noi_dung=request.data['noi_dung'],
            user=request.user,
            cuahang=self.get_object()
        )

        c.save()

        return Response(CommentCuaHangSerializer(c, context={"request": request}).data, status=status.HTTP_201_CREATED)


class CommentCuaHangViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = CommentCuaHang.objects.all()
    serializer_class = CommentCuaHangSerializer
    pagination_class = CommentMonAnPaginator

    def filter_queryset(self, queryset):
        q = queryset
        cuahang_id = self.request.query_params.get('cuahang_id')

        return q.filter(cuahang__id=cuahang_id).order_by('-created_date') if cuahang_id else []


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser, ]

    def get_permissions(self):
        if self.action in ['current_user', 'my_stores']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get', 'put'], detail=False, url_path='current_user')
    def current_user(self, request):
        u = request.user
        if request.method.__eq__('PUT'):
            for k, v in request.data.items():
                setattr(u, k, v)
            u.save()

        return Response(UserSerializer(u, context={'request': request}).data)

    @action(methods=['get', 'post'], detail=False, url_path='my_stores')
    def my_stores(self, request):
        u = request.user
        if request.method.__eq__('GET'):
            results = CuaHang.objects.filter(user_id=u.id)
            print(results)
            return Response(CuaHangSerializer(results, many=True, context={"request": request}).data)

        if request.method.__eq__('POST'):
            results = CuaHang(
                name=request.data['name'],
                address=request.data['address'],
                image=request.data['image'],
                user_id=u.id
            )
            results.save()
            return Response(CuaHangSerializer(results, context={"request": request}).data,
                            status=status.HTTP_201_CREATED)


class DonHangViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = DonHang.objects.all()
    serializer_class = DonHangSerializer
