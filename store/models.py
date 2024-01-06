from django.db import models
from PIL import Image

class Item(models.Model):
    pln = 'PLN'
    usd = 'USD'
    euro = 'Euro'
    currencies = [
        (pln, 'PLN'),
        (usd, 'United States dollar'),
        (euro, 'EURO')
        ]

    image = models.ImageField(upload_to='item_images/')  
    price = models.IntegerField(default=0)
    category = models.CharField(max_length=40, default="Other")
    name = models.CharField(max_length=40)
    currency = models.CharField(max_length=20,
                                choices = currencies,
                                default= pln)
    symbol = models.CharField(max_length=20, default="")
    description = models.CharField(max_length=200)
    delivery_price = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
    def __str__(self):
        return str(self.pk)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        max_width = 200  
        width_percent = (max_width / float(img.size[0]))
        max_height = int((float(img.size[1]) * float(width_percent)))
        img = img.resize((max_width, max_height), Image.LANCZOS)
        img.save(self.image.path)
        
        