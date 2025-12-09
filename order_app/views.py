
from django.shortcuts import render, redirect, get_object_or_404

from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin

from cart_app.utils import get_user_cart

from cart_app.models import CartItem

from .models import Order, OrderItemModel,Payment

from django.conf import settings


import razorpay


class CheckoutView(LoginRequiredMixin, View):
    """
    GET  -> show checkout page with cart summary + address form
    POST -> create Order + OrderItemModel from cart, clear cart, show success
    """

    def get(self, request):

        cart = get_user_cart(request.user)

        cart_items = cart.items.select_related("product").all()

        if not cart_items.exists():
            # if cart empty, send back to cart page
            return redirect("cart_details")

        context = {
            "cart": cart,
            "cart_items": cart_items,
        }
        return render(request, "checkout.html", context)

    def post(self, request):

        cart = get_user_cart(request.user)

        cart_items = cart.items.select_related("product").all()

        if not cart_items.exists():

            return redirect("cart_details")

        # read address / contact from form
        full_name = request.POST.get("full_name")

        phone = request.POST.get("phone")

        address_line1 = request.POST.get("address_line1")

        address_line2 = request.POST.get("address_line2", "")

        city = request.POST.get("city", "")

        postal_code = request.POST.get("postal_code", "")

        # compute total price
        total_price = sum(item.subtotal for item in cart_items)

        # create Order
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            postal_code=postal_code,
            total_price=total_price,
            status="PENDING",
        )

        # create OrderItemModel entries
        order_items = []

        for item in cart_items:

            order_items.append(
                OrderItemModel(
                    order=order, #above order 
                    product=item.product,#loop item means  in car_item has shoe qty2 ,tshirt 3 then   1) item = product = shoe ,qty=1
                    quantity=item.quantity,
                    size=item.size,
                    price=item.product.price,
                )
            )

        OrderItemModel.objects.bulk_create(order_items)

        # clear cart
        cart_items.delete()

        return redirect("order_payment", pk=order.id)


class OrderListView(LoginRequiredMixin, View):
    """
    Show all orders of the logged-in user
    """
    def get(self, request):

        orders = Order.objects.filter(user=request.user).order_by("-created_at")

        context = {"orders": orders}

        return render(request, "order_list.html", context)


class OrderDetailView(LoginRequiredMixin, View):
    """
    Show a single order with items
    """
    def get(self, request, **kwargs):

        order_id = kwargs.get('pk')

        order = get_object_or_404(Order, id=order_id, user=request.user)

        context = {"order": order}

        return render(request, "order_details.html", context)

class OrderPaymentView(LoginRequiredMixin, View):

    template_name = "payment.html"  

    def get(self, request, **kwargs):

        pk = kwargs.get('pk')
       
        order = get_object_or_404(Order, id=pk, user=request.user)

        amount = int(order.total_price * 100)

        # 3) Create Razorpay order This creates a Razorpay client using your API keys.It’s like logging in to Razorpay from your backend.

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


        # You tell Razorpay: “Please create an order for 99900 paise in INR”  payment_capture = 1 → auto capture the payment.

        # Razorpay returns something like:

        # {
        # #   "id": "order_ABC123",
        # #   "amount": 99900,
        # #   ...
        # # }That whole dict is stored in razorpay_order.


        razorpay_order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1,
        })


        # Razorpay’s unique order ID.

        rp_order_id = razorpay_order["id"]

        # Django checks if there’s already a Payment row for this order.
        # 1)First time Anjali is paying for this order
        # 2)She tried before, but payment failed / refreshed page
        
        payment, created = Payment.objects.get_or_create(
            order=order,
            defaults={
                "user": request.user,
                "amount": amount,
                "razorpay_order_id": rp_order_id,
            },
        )
        if not created:
            payment.amount = amount

            payment.razorpay_order_id = rp_order_id

            payment.is_paid = False

            payment.save()

        # 5) Render Razorpay payment page
        context = {
            "order": order,
            "payment": payment,
            "amount": amount,
            "key_id": settings.RAZORPAY_KEY_ID,   # your public key
        }
        return render(request, "payment.html", context)


class PaymentSuccessView(View):
   
    def post(self, request):

        rp_payment_id = request.POST.get("razorpay_payment_id")

        rp_order_id   = request.POST.get("razorpay_order_id")

        rp_signature  = request.POST.get("razorpay_signature")

        payment_db_id = request.POST.get("payment_db_id")   # hidden field in template

        # our Payment row
        payment = get_object_or_404(
            Payment,
            id=payment_db_id,
            razorpay_order_id=rp_order_id,
        )
        order = payment.order

        # store Razorpay details
        payment.razorpay_payment_id = rp_payment_id

        payment.razorpay_signature  = rp_signature

        payment.is_paid = True

        payment.save()

        #  update order status
        order.status = "PAID"

        order.save()

        # go to order details page
        return redirect("order_detail", pk=order.id)
