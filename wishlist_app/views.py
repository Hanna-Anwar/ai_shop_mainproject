from django.shortcuts import render,redirect,get_object_or_404

from django.views.generic import View,ListView

from django.contrib.auth.mixins import LoginRequiredMixin

from product_app.models import ProductModel

from wishlist_app.models import WishlistItem

class AddToWishlistView(LoginRequiredMixin, View):
    """
    Add a product to the user's wishlist.
    """

    def get(self, request, **kwargs):

        product_id = kwargs.get('pk')

        product = get_object_or_404(ProductModel, id=product_id)

        WishlistItem.objects.get_or_create( user=request.user, product=product)

        return redirect("wishlist_details")
    

class WishlistDetailView(LoginRequiredMixin, ListView):

    """
    Show all products in the user's wishlist (ListView version).
    """
    model = WishlistItem

    template_name = "wishlist_detail.html"

    context_object_name = "items"   

    def get_queryset(self):

        # only show wishlist items of the logged-in user
        return WishlistItem.objects.filter(user=self.request.user).select_related("product")
        
# Without select_related("product"):

# Django asks the database many times:

# 1 time to get all wishlist items

# then again for product 5

# again for product 7

# So: many small trips to the database.

# With select_related("product"):

# Django asks the database one time:

# “Give me all wishlist items and their related products together.”


class WishlistRemoveView(LoginRequiredMixin, View):
    """
    Remove one product from wishlist.
    """

    def post(self, request,**kwargs):
       
        item_id = kwargs.get("pk")

        item = get_object_or_404(WishlistItem,id=item_id,user=request.user)

        item.delete()
        
        return redirect("wishlist_details")


