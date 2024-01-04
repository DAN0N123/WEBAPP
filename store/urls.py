from . import views
from django.urls import path

app_name = "store"

urlpatterns = [
    path("homepage/", views.homepage, name="homepage"),
]