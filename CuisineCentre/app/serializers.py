from rest_framework.serializers import ModelSerializer
from .models import MonAn

class MonAnSerializer(ModelSerializer):
    class Meta:
        model = MonAn
        fields = ['id', 'name', 'price', 'loaimonan']

