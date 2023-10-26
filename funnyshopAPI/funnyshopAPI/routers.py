from shop.viewsets import ProductViewSet, \
                            CategoryViewSet
from cart.viewsets import CartViewSet
from orders.viewsets import OrderViewSet
from payment.viewsets import PaymentViewSet
from authentication.viewsets.login import LoginViewSet
from authentication.viewsets.refresh import RefershViewSet


from rest_framework import routers
router = routers.SimpleRouter()


router.register(r'product',
                ProductViewSet,
                basename = 'product')

router.register(r'category',
                CategoryViewSet,
                basename = 'category')

router.register(r'cart',
                CartViewSet,
                basename = 'cart')

router.register(r'order',
                OrderViewSet,
                basename = 'order')

router.register(r'payment',
                PaymentViewSet,
                basename = 'payment')

router.register(r'login',
                LoginViewSet,
                basename = 'login')

router.register(r'refresh',
                RefershViewSet,
                basename = 'refresh')


urlpatterns = [
    *router.urls,

]