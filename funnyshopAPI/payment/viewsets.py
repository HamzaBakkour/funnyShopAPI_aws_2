from rest_framework.viewsets import ViewSet
from orders.models import Order
from rest_framework.response import Response
import stripe
from decimal import Decimal
from rest_framework import status
from django.conf import settings
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .tasks import payment_completed
from cart.cart import Cart
from orders.serializers import OrderSerializer




class PaymentViewSet(ViewSet):
    http_method_names = ('post')


    # create a checkout session
    @action(methods=['post'], detail=False)
    def check_out_session(self, request):
        try:
            order_id = request.session.get('order_id', None)
        except KeyError:
            return Response("No order_id was found in the current session",
                            status=status.HTTP_400_BAD_REQUEST)


        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response("No order was found with the given order_id",
                            status=status.HTTP_400_BAD_REQUEST)

        # Stripe checkout session data
        session_data = {
            'mode': 'payment', #We use payment for a one-time payment.
            'client_reference_id': order.id, #The unique reference for this payment.
            'success_url': "https://funnyshop.hamzabakkour.se/success", #: The URL for Stripe to redirect the user to if the payment is successful.
            'cancel_url': "https://funnyshop.hamzabakkour.se/failed",
            'line_items': []
        }

        for item in order.items.all():
            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': int(item.price * Decimal('100')), #[1]
                    'currency': 'sek',
                    'product_data': {
                        'name': item.product.name,
                    },
                },
                'quantity': item.quantity,
            })


        # create the Stripe instance
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.api_version = settings.STRIPE_API_VERSION

        session = stripe.checkout.Session.create(**session_data)

        return Response(session.url, status=status.HTTP_201_CREATED)
    
    
    @csrf_exempt
    @action(methods=['post'], detail=False)
    def webhook(self, request):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
                        payload,
                        sig_header,
                        settings.STRIPE_WEBHOOK_SECRET)
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)

        if event.type == 'checkout.session.completed':
            session = event.data.object
            if session.mode == 'payment' and session.payment_status == 'paid':
                try:
                    order = Order.objects.get(id=session.client_reference_id)
                except Order.DoesNotExist:
                    return HttpResponse(status=404)
                # mark order as paid
                order.paid = True
                # store Stripe payment ID
                order.stripe_id = session.payment_intent
                order.save()
                # launch asynchronous task
                payment_completed.delay(order.id)
        return HttpResponse(status=200)
