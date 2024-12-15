from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path("", views.index, name="index"),
    path("addPerson", views.addPerson, name="addPerson"),
    path("addPerson_get", views.addPerson_get, name="addPerson_get"),
    path("addRequest", views.addRequest, name="addRequest"),
    path("addRequest_get", views.addRequest_get, name="addRequest_get"),
]