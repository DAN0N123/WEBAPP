from django.shortcuts import render
from store.models import Item
def item_operations(items):
    for item in items:
        item.total_price = item.price + item.delivery_price
        match item.currency:
            case 'PLN':
                item.symbol = 'zł'
            case 'USD':
                item.symbol = '$'
            case 'Euro':
                item.symbol = '€'

def homepage(request):
    items = Item.objects.all()
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    if query:
        items = Item.objects.filter(name__icontains=query)
    if category:
        items = Item.objects.filter(category=category)
    item_operations(items)
    return render(request, 'homepage.html', {'items':items})

