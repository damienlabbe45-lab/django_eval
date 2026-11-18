from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

app_name = "skills"
urlpatterns = [
    path("search_skills/", views.SkillsUserView.as_view(), name="search_skills"),
    path("all_skills/", views.AllskillsView.as_view(), name="all_skills"),
    path("add_skills/", views.create_skills_user, name="add_skills"), # type: ignore
    path("deconnection/", LogoutView.as_view(next_page="skills:index"), name="deconnection"),
    path("connection/", LoginView.as_view(template_name = "skills/connection.html", next_page = "skills:index"), name = "connection"),
    path("", views.IndexView.as_view(), name="index"),
]