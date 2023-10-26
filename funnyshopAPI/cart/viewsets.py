from rest_framework.viewsets import ViewSet
from shop.models import Product
from .cart import Cart
from shop.permissions import UserPoermission
from rest_framework.response import Response
from rest_framework import status
from shop.serializers import ProductSerializer
from rest_framework.decorators import action
# impo

class CartViewSet(ViewSet):
    http_method_names = ('get', 'post', 'delete', 'patch', 'options', 'head', 'trace')



    def list(self, request):
        cart = Cart(request)
        return Response(cart.get_cart_items(), status = status.HTTP_200_OK)


    def create(self, request):
        cart = Cart(request)

        try:
            product = Product.objects.get(id=request.data['product_id'])
            product_image = request.build_absolute_uri(Product.objects.get(id=request.data['product_id']).image.url)

        except Product.DoesNotExist:
            return Response({"Product ID: {} does not exist".format(request.data['product_id'])},
                            status = status.HTTP_404_NOT_FOUND)
        

        cart.add(product,
                    override_quantity=True,
                    quantity=request.data['quantity'],
                    product_image=product_image)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data, status = status.HTTP_200_OK)


    def destroy(self, request, pk=None):
        cart = Cart(request)
        if pk :
            product = Product.objects.get(id=pk)
            if cart.item_exist(pk):
                cart.remove(product)
                serializer = ProductSerializer(product, context={'request': request})
                return Response(serializer.data, status = status.HTTP_200_OK )
            return Response({"Product ID: {} is not in cart". \
                                format(pk)},
                                status = status.HTTP_404_NOT_FOUND )
        else:
            cart.clear()
            return Response(status = status.HTTP_200_OK)


    @action(methods=['delete'], detail=False)
    def clear(self, request):
        cart = Cart(request)
        cart.clear()
        return Response(status = status.HTTP_200_OK)


    @action(methods=['get'], detail=False)
    def get_total_price(self, request):
        cart = Cart(request)
        res = cart.get_total_price()
        return Response(res ,status = status.HTTP_200_OK)