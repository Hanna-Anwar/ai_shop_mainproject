from django.db import models

from user_app.models import CustomUserModel

from product_app.models import ProductModel


class Cart(models.Model):

    user = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)


    @property
    def total_price(self):

        return sum(item.subtotal for item in self.items.all())


class CartItem(models.Model):

    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)

    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)

    size = models.CharField(max_length=10, blank=True, null=True)

   
    @property
    def subtotal(self):
        
        return self.product.price * self.quantity

