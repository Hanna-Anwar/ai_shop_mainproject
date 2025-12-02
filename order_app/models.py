from django.db import models

# from user_app.models import CustomUserModel

# from product_app.models import ProductModel


# class Order(models.Model):

#     STATUS_CHOICES = [
#         ("PENDING", "Pending"),
#         ("PAID", "Paid"),
#         ("CANCELLED", "Cancelled"),
#     ]


#     user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)

#     created_at = models.DateTimeField(auto_now_add=True)
    
#     full_name = models.CharField(max_length=100)

#     address = models.TextField()

#     city = models.CharField(max_length=100)

#     state = models.CharField(max_length=100)

#     pincode = models.CharField(max_length=20)

#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    
#     def __str__(self):

#         return f"Order #{self.id} - {self.user.username}"


# class OrderItemModel(models.Model):

#     order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)

#     product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)

#     size = models.CharField(max_length=10, blank=True, null=True)

#     quantity = models.PositiveIntegerField(default=1)

#     price = models.DecimalField(max_digits=10, decimal_places=2)  # copy at time of order

#     def __str__(self):

#         return f"{self.product.name} x {self.quantity}"
    
# class PaymentModel(models.Model):

#     PAYMENT_METHOD_CHOICES = [
#                         ("COD", "Cash on Delivery"),
#                         ("ONLINE", "Online Payment"),
#     ]

#     PAYMENT_STATUS_CHOICES = [
#                         ("PENDING", "Pending"),
#                         ("SUCCESS", "Success"),
#                         ("FAILED", "Failed"),
#     ]

#     order = models.ForeignKey(Order, related_name="payments", on_delete=models.CASCADE)

#     amount = models.DecimalField(max_digits=10, decimal_places=2)

#     method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)

#     status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default="PENDING")

#     transaction_id = models.CharField(max_length=100, blank=True, null=True)  # for gateway ref

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):

#         return f"Payment for Order #{self.order.id} - {self.status}"

#not done migrations or any thing