import os
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
#from django.contrib.auth.models import User
#from django.utils import timezone
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from shop.settings import AUTH_USER_MODEL


class Category(models.Model):
    GENDER_CHOICES = (
        ('Homme', 'Homme'),
        ('Femme', 'Femme'),
        ('Chaussures', 'Chaussures'),  # Pour les chaussures sans genre
    )

    class Meta:
        verbose_name_plural = 'categories'

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default='Chaussures'
    )

    def __str__(self):
        return self.get_gender_display()

    def get_gender_display(self):
        if self.gender == 'Chaussures':
            return 'Chaussures'
        else:
            return f"Chaussures pour {self.gender}"

class ShoeType(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

def get_product_image_upload_path(instance, filename):
    # Récupérer le nom du produit
    product_name = slugify(instance.name)
    # Concaténer le nom du produit avec le nom du fichier
    path = os.path.join("shoes", product_name, filename)
    return path


class Color(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    # Couleurs préremplies
    COLORS = [
        'Rouge',
        'Bleu',
        'Vert',
        'Jaune',
        'Noir',
        'Blanc',
        'Rose',
        'Violet',
        'Orange',
        'Marron',
        'Gris',
    ]

    @classmethod
    def prepopulate_colors(cls):
        for color in cls.COLORS:
            cls.objects.get_or_create(name=color)

@receiver(post_migrate)
def on_post_migrate(sender, **kwargs):
    from .models import Color
    Color.prepopulate_colors()


class Shoe(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ImageField(upload_to=get_product_image_upload_path, blank=True, null=True)
    colors = models.ManyToManyField(Color)
    stock = models.IntegerField(default=0)
    shoe_type = models.ForeignKey(ShoeType, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.stock})"

    def get_type_display(self):
        return self.shoe_type.name

    def get_colors_display(self):
        return ", ".join([color.name for color in self.colors.all()])

    def get_absolute_url(self):
        return reverse("shoe", kwargs={"slug": self.slug})

class Order(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_completed = models.BooleanField(default=False)
    order_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Article de commande - {self.shoe.name} ({self.quantity}) - Is Completed: {self.is_completed} - Order Date: {self.order_date}"

class Cart(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)

    def __str__(self):
        return f"Cart for {self.user.username} - products ({self.orders.count()})"

    def delete(self, *args, **kwargs):
        for order in self.orders.all():
            order.is_completed = True
            order.order_date = timezone.now()
            order.save()

        self.orders.clear()
        super().delete(*args, **kwargs)



"""class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Commande de {self.user.username} ({self.order_date})"

    class Meta:
        verbose_name_plural = 'order items'"""

"""
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE, related_name='favorites')

    def __str__(self):
        return f"{self.user.username} - {self.shoe.name}"

    class Meta:
        verbose_name_plural = 'favorites'

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.shoe.name} (Qty: {self.quantity})"

    class Meta:
        verbose_name_plural = 'cart items'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    items = models.ManyToManyField(CartItem)
    order_date = models.DateTimeField(default=timezone.now)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Commande de {self.user.username} ({self.order_date})"

    class Meta:
        verbose_name_plural = 'orders'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Article de commande - {self.shoe.name}"

    class Meta:
        verbose_name_plural = 'order items'

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message de {self.name} ({self.subject})"

    class Meta:
        verbose_name_plural = 'contact messages'

class AboutPage(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

class TermsAndConditionsPage(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

class PrivacyPolicyPage(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

class FAQPage(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
"""