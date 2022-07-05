
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("profile/<int:user_id>", views.profile, name="profile"),
    path("profile/<int:user_id>/follow", views.following, name="following"),
    path("follow", views.follow, name="follow"),

    path("new", views.new, name="new"),    
]
