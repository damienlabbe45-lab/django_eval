from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

app_name = "skills"
urlpatterns = [
    path("deconnection/", LogoutView.as_view(next_page="polls:index"), name="deconnection"),
    path("connection/", LoginView.as_view(template_name = "polls/connection.html", next_page = "polls:index"), name = "connection"),
    path("", views.IndexView.as_view(), name="index"),
]