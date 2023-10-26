from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer, \
                            OrderItemSerializer
from cart.cart import Cart
from .tasks import order_created
from .models import Order
from shop.permissions import UserPoermission

class OrderViewSet(ModelViewSet):
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (UserPoermission,)
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.all()

    def get_object(self):

        obj = Order.objects.get(id=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request):
        
        cart = Cart(request)

        if len(cart.get_cart_items()) == 0:
            return Response({ "Cart is empty" },
                            status=status.HTTP_400_BAD_REQUEST)

        order_serializer = self.get_serializer(data=request.data)
        order_serializer.is_valid(raise_exception=True)
        self.perform_create(order_serializer)


        for item in cart.get_cart_items():

            item_serializer = OrderItemSerializer(data={
                'order': order_serializer.data['id'],
                'product': item,
                'quantity': cart.get_cart_items()[item]['quantity'],
                'price': cart.get_cart_items()[item]['price']
            })
            item_serializer.is_valid(raise_exception=True)
            item_serializer.save()

        order_created.delay(order_serializer.data,
                            cart.get_cart_items(),
                            len(cart),
                            cart.get_total_price()
                            )


        request.session['order_id'] = order_serializer.data['id']


        cart.clear()
        return Response(order_serializer.data,
                        status=status.HTTP_201_CREATED)

