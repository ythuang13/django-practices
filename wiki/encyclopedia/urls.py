from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.get_entry, name="entry"),
    path("random", views.get_random, name="random"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new"),
    path("error/<str:title>", views.error, name="error"),
    path("wiki/<str:title>/edit", views.edit_entry, name="edit")
]
