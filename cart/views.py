from django.shortcuts import render,redirect
from django.conf import settings
from .cart import Cart
from django.http import HttpResponse
from django.template.loader import render_to_string
from product.models import Product
from django.contrib.auth.decorators import login_required

def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)

    if request.headers.get('Hx-Request') == 'true':
        html = render_to_string('cart/partials/menu_cart.html', {'cart': cart})
        response = HttpResponse(html)
        response['HX-Trigger'] = 'update-menu-cart'  # triggers cart total update
        return response

    return redirect('cart')

def cart(request):
    cart=Cart(request)
    return render(request,'cart/cart.html',{'cart':cart})

def success(request):
    return render(request,'cart/success.html')

def update_cart(request, product_id, action):
    cart = Cart(request)

    if action == 'increment':
        cart.add(product_id, 1, True)
    else:
        cart.add(product_id, -1, True)

    product = Product.objects.get(pk=product_id)
    quantity = cart.get_item(product_id)

    if quantity:
        quantity = quantity['quantity']
        item = {
            'product': {
                'id': product.id,
                'slug': product.slug,  # ✅ Add this line
                'name': product.name,
                'image': product.image,
                'get_thumbnail': product.get_thumbnail(),
                'price': product.price,
            },
            'total_price': (quantity * product.price) / 100,
            'quantity': quantity,
        }
    else:
        item = None

    response = render(request, 'cart/partials/cart_item.html', {'item': item})
    response['HX-Trigger'] = 'update-menu-cart'
    return response


@login_required
def checkout(request):
    pub_key = settings.STRIPE_API_KEY_PUBLISHABLE
    cart = Cart(request)
    return render(request, 'cart/checkout.html', {
        'pub_key': pub_key,
        'cart': cart,
    })


def hx_menu_cart(request):
    cart=Cart(request)
    return render(request,'cart/partials/menu_cart.html',{'cart':cart})

def hx_cart_total(request):
    cart=Cart(request)
    return render(request,'cart/partials/cart_total.html',{'cart':cart})