from django.shortcuts import render, redirect
from django.urls import reverse
from store.models import Item
from store.forms import SellItemForm, LoginForm, RegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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
            return redirect(reverse('store:homepage'))  
        # else:
        #     print(form.errors)
    else:
        form = SellItemForm()
    
    return render(request, 'sell_item.html', {'form':form})


def loginstore(request):
    if request.method == 'POST':
        form = LoginForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You Have Been Logged In")
                return redirect(reverse('store:homepage')) 
            else:
                messages.success(request, "This user does not exist")

    else:
        form = LoginForm()
    return render(request, "loginstore.html", {'form':form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You Have Been Registered")
                return redirect(reverse('store:homepage')) 
    else:
        form = RegistrationForm()
    return render(request, "registerstore.html", {'form':form})

def logoutstore(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out")
    return redirect(reverse("store:homepage"))

def itemdisplay(request):
    id = request.GET.get('id', '')
    item = Item.objects.get(pk=id)
    item_operations([item])
    return render(request, "item.html", {'item':item})
