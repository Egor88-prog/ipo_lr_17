from django.db import models
from django.core.validators import MinValueValidator


class Category(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    def __str__(self):
        return self.name

class Manufacture(models.Model):
    name=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    descriptions=models.TextField()
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name=models.CharField(max_length=200)
    descriptions=models.TextField()
    img_product=models.ImageField()
    price=models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    quantity=models.IntegerField(validators=[MinValueValidator(0)])
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    manufacture=models.ForeignKey(Manufacture,on_delete=models.CASCADE)
    def __str__(self):
        return self.name