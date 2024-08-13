from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=100)
    origin_country = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Device(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    display_size = models.CharField(max_length=10)
    in_stock = models.BooleanField(default=True)
    origin_country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.model} ({self.brand.name})"
