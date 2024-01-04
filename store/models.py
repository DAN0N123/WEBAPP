from django.db import models



class Item(models.Model):
    image = models.ImageField(width_field=300, height_field=300)
    price = models.CharField(max_length=30, default = "")
    category = models.CharField(max_length=40, default= "General")
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=200)
    def __str__(self):
        return str(self.pk)