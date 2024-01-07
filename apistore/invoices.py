import requests

from store.models import Order
from django.conf import settings


def create_invoice(order: Order, webhook_url):
    amount = 0
    basket_order = []
    for qty in order.car_types.all():
        sum_ = qty.car_type.price * qty.quantity
        amount += sum_
        basket_order.append(
            {"name": qty.car_type.name, "qty": qty.quantity, "sum": sum_}
        )

    merchants_info = {
        "reference": str(order.id),
        "destination": "Buying cars",
        "basketOrder": basket_order,
    }
    request_body = {
        "webHookUrl": webhook_url,
        "amount": amount,
        "merchantPaymInfo": merchants_info,
    }
    headers = {"X-Token": settings.MONOBANK_TOKEN}

    request = requests.post(
        "https://api.monobank.ua/api/merchant/invoice/create",
        json=request_body,
        headers=headers,
    )
    order.order_id = request.json()["invoiceId"]
    order.save()
