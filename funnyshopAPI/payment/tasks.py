from celery import shared_task
from orders.models import Order
from orders.models import Order
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@shared_task
def payment_completed(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully paid.
    """
    order = Order.objects.get(id=str(order_id))


    email_subject = "FunnyShop Pokemon Payment success"
    email_of_sender = 'alexander.x4.hb@outlook.com'
    email_of_recipient = order.email


    context = ({
                "order_id": order.id,
                "first_name": order.first_name,
                "last_name": order.last_name,}) 

    text_content = render_to_string('payment_success.txt', context)
    html_content = render_to_string('payment_success.html', context)

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




