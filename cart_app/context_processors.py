# cart_app/context_processors.py

# from .models import Cart


# def cart_count(request):
#     """
#     Provide {{ cart_count }} to all templates.
#     Uses the user-based Cart model (one cart per user).
#     """

#     # if user is not logged in, no cart
#     if not request.user.is_authenticated:

#         return {"cart_count": 0}

#     try:

#         cart = Cart.objects.get(user=request.user)

#     except Cart.DoesNotExist:

#         return {"cart_count": 0}

#     # total quantity of all items in the cart
#     total = 0

#     for item in cart.items.all(): 

#           # 'items' is the related_name on CartItem

#         total += item.quantity

#     return {"cart_count": total}

# cart_app/context_processors.py

from django.db.models import Sum
from cart_app.models import CartItem


def cart_count(request):
    """
    Provides {{ cart_count }} for all templates.
    Counts all CartItem rows that belong to carts of the current user.
    """

    # Not logged in ⇒ no user cart
    if not request.user.is_authenticated:
        return {"cart_count": 0}

    # Count CartItem objects for this user, across all their carts (normally 1)
    total = (
        CartItem.objects
        .filter(cart__user=request.user)    # follow FK: CartItem.cart -> Cart.user
        .aggregate(total=Sum("quantity"))["total"]
        or 0
    )

    return {"cart_count": total}

