from django.shortcuts import render
from store.models import Item

def homepage(request):
    items = Item.objects.all()
    return render(request, 'homepage.html', {'items':items})
