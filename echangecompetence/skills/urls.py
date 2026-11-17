from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

app_name = "skills"
urlpatterns = [
    path("add_skills", views.IndexView.as_view(), name="add_skills"),
    path("deconnection/", LogoutView.as_view(next_page="skills:index"), name="deconnection"),
    path("connection/", LoginView.as_view(template_name = "skills/connection.html", next_page = "skills:index"), name = "connection"),
    path("", views.IndexView.as_view(), name="index"),
]