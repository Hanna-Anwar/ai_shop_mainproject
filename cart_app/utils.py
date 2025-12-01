"""Every logged-in user should have one cart.

When you call get_user_cart(request.user), this function:

Looks in the database:
“Is there already a Cart for this user?”

If yes → returns that existing cart.
If no → creates a new Cart for this user and then returns it.

So you always get a valid Cart object, and you don’t have to write the same code again and again."""


from .models import Cart

def get_user_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart
