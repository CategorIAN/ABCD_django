from django.urls import path
from . import views

app_name = "app"

urlpatterns = [
    path("", views.index, name="index"),
    path("updatePerson", views.updatePerson, name="updatePerson"),
    path("updatePerson_get", views.updatePerson_get, name="updatePerson_get"),
    path("addRequest", views.addRequest, name="addRequest"),
    path("addRequest_get", views.addRequest_get, name="addRequest_get"),
    path("addInvitation", views.addInvitation, name="addInvitation"),
    path("addInvitation_get/<event>/", views.addInvitation_get, name="addInvitation_get"),
    path("personalProfile", views.personalProfile, name="personalProfile"),
    path("personalProfile_get/<person>/", views.personalProfile_get, name="personalProfile_get"),
    path("games", views.games, name="games"),
    path("games_get/<game>/", views.games_get, name="games_get"),
    path("eventplans", views.event_plans, name="event_plans"),
    path("eventplans_get/<event_plan>/", views.event_plans_get, name="event_plans_get"),
]