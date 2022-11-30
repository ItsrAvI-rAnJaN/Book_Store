from django.db import models
from book.models import Book
from user.models import User


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        price = sum([item.price for item in self.cartitem_set.all()])
        return price

    @property
    def cartitem(self):
        try:
            return self.cartitem_set.all()
        except Exception:
            return []


class CartItem(models.Model):
    price = models.DecimalField(max_digits=20, decimal_places=3)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

