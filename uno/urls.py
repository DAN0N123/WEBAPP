from . import views
from django.urls import path

app_name = "uno"

urlpatterns = [
    path("homepage/", views.homepage, name="homepage"),
    path("register/", views.register_user, name="register"),
    path("logout/", views.logout_user, name="logout"),
    path("login/", views.login_user, name="login"), 
    path("add_post/", views.add_post, name="add_post"),
    path("like/", views.like, name="like"),
    path("dislike/", views.dislike, name="dislike"),
    path("edit_post/", views.edit_post, name="edit_post"),
    path('delete_post/', views.delete_post, name="delete_post"),
    path('add_comment/', views.add_comment, name = "add_comment"),
    path('comments/', views.comments, name="comments"),
]
