from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = "store"

urlpatterns = [
    path("homepage/", views.homepage, name="homepage"),
    path("sell_item/", views.sell_item, name="sell_item"),
    path("login/", views.loginstore, name="login"),
    path("register/", views.register, name="register"),
    path("logout", views.logoutstore, name="logout"),
    path("item/", views.itemdisplay, name="item"),
    path("add_to_cart/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart , name="cart")
]