from django.shortcuts import render, redirect
from django.urls import reverse
from store.models import Item,  CustomUser, Message
from store.forms import SellItemForm, LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Sum

def homepage(request):
    items = Item.objects.all()
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    user = request.user
    messages = None
    if user.username:
        user.messages.clear()
        for i in range(0,5):
            message = Message.objects.create(message="Hello World")
            user.messages.add(message)
        messages = reversed(user.messages.all())
    if query:
        items = Item.objects.filter(name__icontains=query)
        items = reversed(items)
        return render(request, 'homepage.html', {'items':items,'user_messages':messages, 'query':query})
    if category:
        items = items.filter(category__name__iexact=category)
    items = reversed(items)
    return render(request, 'homepage.html', {'items':items, 'user_messages': messages})
    
    

def sell_item(request):
    if request.method == 'POST':
        form = SellItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save()
            return redirect(reverse('store:homepage'))  
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
    user = request.user
    user_messages = None
    if user.username:
        if len(user.messages.all()) == 0:
            message = Message.objects.create(message="Hello World")
            user.messages.add(message)
        user_messages = reversed(user.messages.all())
    return render(request, "item.html", {'item':item, "user_messages":user_messages})

def add_to_cart(request):
    id = request.GET.get('id','')
    user_id = request.GET.get('user_id', '')
    item = Item.objects.get(pk=id)
    user = CustomUser.objects.get(pk=user_id)
    user.cart.add(item)
    return redirect(reverse("store:cart") + f'?user_id={user_id}')

def cart(request):
    user = request.user
    cart = user.cart.all()
    user_messages = None
    if user.username:
        if len(user.messages.all()) == 0:
            message = Message.objects.create(message="Hello World")
            user.messages.add(message)
        user_messages = user.messages.all()
    total = cart.aggregate(total_price=Sum('total_price'))['total_price'] or 0
    return render(request, 'cart.html', {'cart': cart, 'user_messages':user_messages, 'total':total})

def favorite_item(request):
    id = request.GET.get('id','')
    user_id = request.GET.get('user_id', '')
    item = Item.objects.get(pk=id)
    user = CustomUser.objects.get(pk=user_id)
    item.favorites += 1
    user.favorites.add(item)
    print(user.favorites.all())
    return redirect(reverse("store:homepage"))

def unfavorite_item(request):
    id = request.GET.get('id','')
    user_id = request.GET.get('user_id', '')
    item = Item.objects.get(pk=id)
    user = CustomUser.objects.get(pk=user_id)
    item.favorites -= 1
    user.favorites.remove(item)
    return redirect(reverse("store:homepage"))

def favorites(request):
    user = request.user
    user_messages = None
    if user.username:
        if len(user.messages.all()) == 0:
            message = Message.objects.create(message="Hello World")
            user.messages.add(message)
        user_messages = user.messages.all()
    favorite_items = user.favorites.all()
    return render(request, 'cart.html', {'favorites': favorite_items, 'user_messages':user_messages})

def deletecart(request):
    id = request.GET.get('id','')
    action = request.GET.get('action')
    item = Item.objects.get(pk=id)
    user = request.user
    if action:
        if action == 'cart':
            user.cart.remove(item)
            cart = (user.cart.all())
            favorite_items = (user.favorites.all())
            user_messages = user.messages.all()
            return redirect(reverse("store:cart") + f'?user_messages={user_messages}&cart={cart}')
        else:
            user.favorites.remove(item)
            cart = (user.cart.all())
            favorite_items = (user.favorites.all())
            user_messages = user.messages.all()
            return redirect(reverse("store:favorites") + f'?user_messages={user_messages}&favorites={favorite_items}')
    
    

