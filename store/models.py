from django.db import models
from PIL import Image
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
other = 'Other'
decoration = 'Decoration'
food = 'Food'
onepiece = 'Onepiece'
electronics = 'Electronics'

CATEGORIES = [
        (other, 'Other'),
        (decoration, 'Decoration'),
        (food, 'Food'),
        (onepiece, 'Onepiece'),
        (electronics, 'Electronics')
    ]

class Category(models.Model):
    name = models.CharField(max_length=40, choices = CATEGORIES, unique=True)
    def __str__(self):
        return self.name
    
other = Category(name='Other')
decoration = Category(name='Decoration')
food = Category(name='Food')
onepiece = Category(name='Onepiece')
electronics = Category(name='Electronics')


class Message(models.Model):
    current_time = timezone.now()
    time_sent = models.CharField(max_length= 50, blank=True)
    message = models.CharField(max_length = 20)
    def save(self, *args, **kwargs):
        if not self.time_sent:
            self.time_sent = timezone.now().strftime('%Y-%m-%d %H:%M')
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.pk)

class Item(models.Model):
    image = models.ImageField(upload_to='item_images/')  
    price = models.IntegerField(default=0)
    category = models.ManyToManyField(Category, blank=True, null=True)
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=200)
    delivery_price = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
    favorites = models.IntegerField(default=0)
    def __str__(self):
        return str(self.pk)
    
    def save(self, *args, **kwargs):
        self.total_price = self.delivery_price + self.price
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        max_height = 250 
        height_percent = (max_height / float(img.size[1]))
        max_width = int((float(img.size[0]) * float(height_percent)))
        img = img.resize((max_width, max_height), Image.LANCZOS)
        img.save(self.image.path)
        
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    cart = models.ManyToManyField(Item, related_name='cart_items', blank=True)
    favorites = models.ManyToManyField(Item, related_name='favorite_items',blank=True)
    date_joined = models.TimeField(default=timezone.now())
    objects = CustomUserManager()
    messages = models.ManyToManyField(Message, related_name='messages', blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        return self.username