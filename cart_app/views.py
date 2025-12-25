from django.shortcuts import render,redirect,get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import View

from cart_app.utils import get_user_cart

from cart_app.models import CartItem

from product_app.models import ProductModel





# LoginRequiredMixin automatically:

# checks request.user.is_authenticated

# if not logged in, redirects to settings.LOGIN_URL

# You don’t need to repeat checks inside get/post.

class AddToCartView(LoginRequiredMixin, View):
  

    def post(self, request,**kwargs):

        product_id = kwargs.get('pk')  
        
        product = get_object_or_404(ProductModel, id=product_id)

        cart = get_user_cart(request.user)

        quantity = int(request.POST.get("quantity", 1))

        size = request.POST.get("size", "")
        
        top_size = request.POST.get("top_size")

        bottom_size = request.POST.get("bottom_size")

        if product.is_set:

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                top_size=top_size if top_size else None,
                bottom_size=bottom_size if bottom_size else None,
                defaults={"quantity": quantity},
            )

            if not created:

                cart_item.quantity += quantity

                cart_item.save()

        # ✅ Normal product -> use single size
        else:

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                size=size if size else None,
                defaults={"quantity": quantity},
            )

            if not created:

                cart_item.quantity += quantity
                
                cart_item.save()

        return redirect("cart_details")

    
class CartDetailView(LoginRequiredMixin, View): 

    def get(self, request):

        cart = get_user_cart(request.user)

        items = cart.items.select_related("product").all()

        # calculate total
        cart_total = sum(item.subtotal for item in items)

        total_items = sum(item.quantity for item in items)

        return render(request, "cart_detail.html", {"cart": cart, "items": items,"cart_total":cart_total,"total_item":total_items})
    
class CartIncreaseView(LoginRequiredMixin, View):
    """
    Increase quantity of a CartItem by 1.
    """
    def post(self, request, **kwargs):

        inc_id = kwargs.get('pk')

        item = get_object_or_404(CartItem, id=inc_id, cart__user=request.user)

        item.quantity += 1

        item.save()

        return redirect("cart_details")
    
class CartDecreaseView(LoginRequiredMixin, View):
    """
    Decrease quantity of a CartItem by 1.
    If it would go to 0, delete the item.
    """
    def post(self, request,**kwargs):

        dec_id = kwargs.get('pk')

        item = get_object_or_404(CartItem, id=dec_id, cart__user=request.user)

        if item.quantity > 1:

            item.quantity -= 1

            item.save()

        else:

            item.delete()

        return redirect("cart_details")
    
class CartRemoveView(LoginRequiredMixin, View):
    """
    Remove a CartItem completely from the cart.
    """

    def post(self, request,**kwargs):

        d_id = kwargs.get('pk')

        item = get_object_or_404(CartItem, id=d_id, cart__user=request.user)

        item.delete()
        
        return redirect("cart_details")



