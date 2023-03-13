from rest_framework import viewsets, permissions
from .models import MonAn
from .serializers import MonAnSerializer


class MonAnViewSet(viewsets.ModelViewSet):
    queryset = MonAn.objects.filter(active=True)
    serializer_class = MonAnSerializer

