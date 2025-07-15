from .models import Order, OrderItem
from cart.cart import Cart
import json
import stripe
from django.http import JsonResponse
from django.conf import settings

def start_order(request):
    cart = Cart(request)
    data = json.loads(request.body)

    stripe.api_key = settings.STRIPE_API_KEY_SECRET
  # ✅ Set API key FIRST

    total_price = 0
    line_items = []

    for cart_item in cart:
        product = cart_item['product']
        quantity = int(cart_item['quantity'])
        total_price += product.price * quantity

        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': product.name},
                'unit_amount': product.price,
            },
            'quantity': quantity
        })

    # ✅ Create only one session
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url='http://127.0.0.1:8000/cart/success/',
        cancel_url='http://127.0.0.1:8000/cart/',
    )

    payment_intent = session.payment_intent

    # ✅ Save order info
    order = Order.objects.create(
        user=request.user,
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data['phone'],
        address=data['address'],
        zipcode=data['zipcode'],
        place=data['place'],
        paid=True,
        paid_amount=total_price,
        payment_intent=payment_intent
    )

    for cart_item in cart:
        product = cart_item['product']
        quantity = int(cart_item['quantity'])
        price = product.price * quantity

        OrderItem.objects.create(
            order=order,
            product=product,
            price=price,
            quantity=quantity
        )
    cart.clear()

    return JsonResponse({'session': session, 'order': payment_intent})
