from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from shop.models import Product


class Profile(models.Model):
    ROLE_CHOICES = [
        ('CUSTOMER', 'Покупатель'),
        ('ADMIN', 'Администратор'),
        ('MANAGER', 'Менеджер'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CUSTOMER')
    full_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True, verbose_name='Город доставки')
    postal_code = models.CharField(max_length=20, blank=True, verbose_name='Индекс')

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"

    def total_price(self):
        return sum(item.item_total_price() for item in self.items.all())



class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.product.name} ({self.quantity} шт.)"

    def item_total_price(self):
        return self.product.price * self.quantity

    def clean(self):
        if self.product and self.quantity > self.product.quantity:
            raise ValidationError(
                f"Недостаточно товара. Доступно: {self.product.quantity}"
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

