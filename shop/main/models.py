from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):

    pass


class Material(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_images_material', default='product_images/Screenshot_1.png')

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images', default='product_images/Screenshot_1.png')
    gallery_images = models.ManyToManyField('GalleryImage', blank=True)
    description = models.CharField(max_length=255)
    materials = models.ManyToManyField(Material, blank=True)
    colors = models.ManyToManyField(Color, blank=True)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    color = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    Success = models.BooleanField(default=False)

    def __str__(self):
        return f"CartItem: {self.user.username} - {self.product.name}"


class GalleryImage(models.Model):
    name = models.CharField(max_length=100, default='')
    image = models.ImageField(upload_to='product_images/gallery')
    product_key = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery')
