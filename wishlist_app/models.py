from django.db import models

from user_app.models import CustomUserModel

from product_app.models import ProductModel

class WishlistItem(models.Model):

    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)

    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        unique_together = ("user", "product")  # same product only once per user

    def __str__(self):

        return f"{self.user.username} → {self.product.name}"
    

# For this model, the pair (user, product) must be unique in the database.

# So:

# One user can have many wishlist items ✅

# One product can be in many users’ wishlists ✅

# But
