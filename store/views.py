from django.shortcuts import render, redirect
from store.models import Item, Category
from store.forms import SellItemForm
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
        items = items.filter(category__name__iexact=category)
    item_operations(items)
    items = reversed(items)
    return render(request, 'homepage.html', {'items':items})

def sell_item(request):
    if request.method == 'POST':
        form = SellItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save()
            return redirect('homepage', pk=item.pk)  
    else:
        form = SellItemForm()
    
    return render(request, 'sell_item.html', {'form':form})

