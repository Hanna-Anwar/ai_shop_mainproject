from django.db import models
from user_app.models import CustomUserModel
from product_app.models import ProductModel


class Order(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
        ("CANCELLED", "Cancelled"),
    ]

    user = models.ForeignKey(
        CustomUserModel,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    # Basic shipping / contact info (from checkout form)
    full_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=15)

    address_line1 = models.CharField(max_length=255)

    address_line2 = models.CharField(max_length=255, blank=True, null=True)

    city = models.CharField(max_length=100, blank=True, null=True)

    postal_code = models.CharField(max_length=20, blank=True, null=True)

    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

    @property
    def item_count(self):

        return sum(item.quantity for item in self.items.all())


class OrderItemModel(models.Model):

    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)

    size = models.CharField(max_length=10, blank=True, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)  # price at time of order

    def __str__(self):

        return f"{self.product.name} x {self.quantity}"

    @property
    def subtotal(self):

        return self.quantity * self.price
