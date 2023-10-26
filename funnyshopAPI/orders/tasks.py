from celery import shared_task
from .models import Order
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


@shared_task
def order_created(order, cart_items, items_count, total_price):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """



    order = Order.objects.get(id=order['id'])


    email_subject = "FunnyShop Pokemon order: {}".format(order.id)
    email_of_sender = 'alexander.x4.hb@outlook.com'
    email_of_recipient = order.email
    cart = []
    for item in cart_items:
        cart.append({
            'product_id': item,
            'name': cart_items[item]['name'],
            'quantity': cart_items[item]['quantity'],
            'price': cart_items[item]['price'],
            'product_image': cart_items[item]['product_image'],
            })
        

    context = ({
                "order_id": order.id,
                "first_name": order.first_name,
                "last_name": order.last_name,
                "cart": cart,
                "total_price": total_price,
                "total_count": items_count}) 

    text_content = render_to_string('order_placed.txt', context)
    html_content = render_to_string('order_placed.html', context)

    try:
        #I used EmailMultiAlternatives because I wanted to send both text and html
        email_message = EmailMultiAlternatives(subject=email_subject,
                                                body=text_content,
                                                from_email=email_of_sender,
                                                to=[email_of_recipient,],
                                                reply_to=[email_of_sender,])

        email_message.attach_alternative(html_content, "text/html")
        email_message.send(fail_silently=False)

    except Exception as e:
        print('There was an error sending an email: ', e) 
        error = {'message': ",".join(e.args) if len(e.args) > 0 else 'Unknown Error'}
        raise Exception(error)

