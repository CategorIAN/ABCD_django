from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path("", views.index, name="index"),
    path("addPerson", views.addPerson, name="addPerson"),
    path("addPerson_get", views.addPerson_get, name="addPerson_get"),
]