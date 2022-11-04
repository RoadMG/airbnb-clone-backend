from rest_framework.viewsets import ModelViewSet
from .serializers import CategorySerializer
from .models import Category


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
