from rest_framework import pagination


class MonAnPaginator(pagination.PageNumberPagination):
    page_size = 3


class CuaHangPaginator(pagination.PageNumberPagination):
    page_size = 3


class CommentMonAnPaginator(pagination.PageNumberPagination):
    page_size = 3


class CommentCuaHangPaginator(pagination.PageNumberPagination):
    page_size = 3

