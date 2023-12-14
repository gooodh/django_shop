from yookassa import Configuration, Payment
import uuid

from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from orders.models import Order


# create the Stripe instance

Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


def payment_process(request):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        success_url = request.build_absolute_uri(
                        reverse('payment:completed'))

        unit_amount = 0
        for item in order.items.all():
            unit_amount = int(item.price)
        get_total_cost = order.get_total_cost()
        currency = 'RUB'
        description = 'Товары в корзине'
        payment = Payment.create({
            "amount": {
                "value": get_total_cost,
                "currency": currency},

            "confirmation": {
                "type": "redirect",
                "return_url": success_url},
            "capture": True,
            "test": True,
            "description": description}, uuid.uuid4())
        confirmation_url = payment.confirmation.confirmation_url

        return redirect(confirmation_url)

    else:
        return render(request, 'payment/process.html', locals())


def payment_completed(request):
    return render(request, 'payment/completed.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')
