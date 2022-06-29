from decimal import Decimal

from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('show_by_category', args=[self.slug])


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    slug = models.SlugField()
    description = RichTextField()
    image = models.ImageField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('show_item', args=[self.slug])


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def __str__(self):
        return f"session: {self.session}, cart:{self.cart}"

    def save(self):
        self.session.modified = True

    def add_product(self, product):
        product_id = str(product.id)
        if product_id not in self.cart.keys():
            self.cart[product_id] = {
                'quantity': '1',
                'price': str(product.price)
            }
        else:
            print('Product already in the cart')
        self.save()

    def cart_len(self):
        return len(self.cart)

    def __len__(self):
        return sum(int(item['quantity']) for item in self.cart.values())

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Item.objects.filter(id__in=product_ids)  # 1 2 3
        # cart:{'1': {'quantity': '1', 'price': '999.0'}}
        for product in products:
            product.quantity = int(self.cart[str(product.id)]['quantity'])
            product.price = Decimal(self.cart[str(product.id)]['price'])
            product.total_price = product.quantity * product.price
            yield product

    def get_total_price(self):
        return sum(Decimal(item['price']) * int(item['quantity']) for item in self.cart.values())

    def remove(self, product):
        if str(product.id) in self.cart.keys():
            del self.cart[str(product.id)]
            self.save()

    def change_quantity(self, product, quantity):
        self.cart[str(product.id)]['quantity'] = quantity
        self.save()

    def clear(self):
        del self.session['cart']
        self.save()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="profiles_images/")
    orders = models.ForeignKey('Order', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"User {self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


