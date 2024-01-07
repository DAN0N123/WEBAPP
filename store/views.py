from django.shortcuts import render, redirect
from django.urls import reverse
from store.models import Item,  CustomUser
from store.forms import SellItemForm, LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError

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
    return items

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
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already exists. Please choose a different one.")
                return render(request, "registerstore.html", {'form': form})

            try:
                user = CustomUser.objects.create_user(username=username, email=email, password=password)
                login(request, user)
                messages.success(request, "You have been registered")
                return redirect(reverse('store:homepage'))
            except IntegrityError:
                messages.error(request, "Error creating user. Please try again.")
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

def add_to_cart(request):
    id = request.GET.get('id','')
    user_id = request.GET.get('user_id', '')
    item = Item.objects.get(pk=id)
    user = CustomUser.objects.get(pk=user_id)
    user.cart.add(item)
    return redirect(reverse("store:homepage"))

def cart(request):
    user_id = request.GET.get('user_id', '')
    user = CustomUser.objects.get(pk=user_id)
    cart = item_operations(user.cart.all())
    return render(request, 'cart.html', {'cart': cart})
