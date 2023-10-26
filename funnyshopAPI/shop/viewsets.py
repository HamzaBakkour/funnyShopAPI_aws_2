from rest_framework.viewsets import ModelViewSet
from .permissions import UserPoermission
from .serializers import ProductSerializer, \
                            CategorySerializer
from .models import Product, \
                        Category
from rest_framework import status
from rest_framework.exceptions import ValidationError



class ProductViewSet(ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (UserPoermission,)
    serializer_class = ProductSerializer
    lookup_field = 'id'


    def get_queryset(self):
        category_slug = self.request.query_params.get('category')

        if category_slug:
            return Product.objects.filter(category__slug=category_slug, \
                                            available=True)
        

        return Product.objects.filter(available=True)


class CategoryViewSet(ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (UserPoermission,)
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()


