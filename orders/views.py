from django.urls import reverse

from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY 

def order_create( request ):
    cart = Cart(request)
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount='{:.0f}'.format(cart.get_total_price()*100),
            currency='DHS',
            description='Pay By Credit Cart',
            source=request.POST['stripeToken']
        )
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()




            # redirect  payment
            request.session.modified = True

            order.paid = True
            # store the unique transaction id
            order.save()

            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        form = OrderCreateForm()
        key = settings.STRIPE_PUBLISHABLE_KEY
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart,'key': key, 'form': form})