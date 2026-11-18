from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator

from django.views import generic


from .models import SkillsDate, Skills, UserSkills
from .forms import SkillsForm
#from .user import create_user
from django.db import connection


class IndexView(generic.ListView):
    template_name = "skills/index.html"
    context_object_name = "latest_skills_date_list"

    def get_queryset(self):
        """Return the last ten skills helping."""
        #with open("C:\\Users\\LabbeD\\OneDrive - Facylities Multi Services\\Documents\\evaldjango\\echangecompetence\\data.sql", 'r', encoding='utf-8') as f:
        #    sql_content = f.read()
            
        #with connection.cursor() as cursor:
        #    cursor.executescript(sql_content)
            
        #create_user() fonction qui a servi à créé les utilisateurs directement
        return SkillsDate.objects.filter(boolean = False ,skills__name_skills__contains='aide ').order_by("-date_before")[
        :10
    ]


class AllskillsView(IndexView):
    template_name = "skills/all_skills.html"

    def get_queryset(self):
            """Return the skills."""
            return Skills.objects.order_by("name_skills")

@method_decorator(login_required(login_url="/skills/connection"), name='dispatch' )# type: ignore
class SkillsUserView(IndexView):
    template_name = "skills/search_skills.html"

    
    def get_queryset(self):
            """Returns users whom the current user can help."""
            with connection.cursor() as con:
                con.execute("""SELECT auth_user.username, skills_useremail.email, skills_skills.name_skills 
                FROM skills_userskills 
                JOIN skills_useremail ON skills_userskills.user_id = skills_useremail.id 
                JOIN auth_user ON skills_useremail.user_id = auth_user.id 
                JOIN skills_skillsdate ON skills_userskills.Skills_id = skills_skillsdate.id 
                JOIN skills_skills ON skills_skillsdate.skills_id = skills_skills.id 
                WHERE skills_useremail.user_id != :auth_id 
                AND skills_skills.name_skills IN (
                    SELECT 'aide pour ' || target_skills.name_skills 
                    FROM skills_userskills target_us
                    JOIN skills_useremail target_ue ON target_us.user_id = target_ue.id
                    JOIN skills_skillsdate target_ssd ON target_us.Skills_id = target_ssd.id
                    JOIN skills_skills target_skills ON target_ssd.skills_id = target_skills.id
                    WHERE target_ue.user_id = :auth_id
                )""", {"auth_id" : self.request.user.id})# type: ignore
                return con.fetchall()

class SkillsUserHelpView(SkillsUserView):
     template_name = "skills/search_help_skills.html"

     def get_queryset(self):
                 """Returns users whom the current user can then help."""
                 with connection.cursor() as con:
                     con.execute("""SELECT auth_user.username, skills_useremail.email, skills_skills.name_skills 
                     FROM skills_userskills 
                     JOIN skills_useremail ON skills_userskills.user_id = skills_useremail.id 
                     JOIN auth_user ON skills_useremail.user_id = auth_user.id 
                     JOIN skills_skillsdate ON skills_userskills.Skills_id = skills_skillsdate.id 
                     JOIN skills_skills ON skills_skillsdate.skills_id = skills_skills.id 
                     WHERE skills_useremail.user_id != :auth_id 
                     AND skills_skills.name_skills IN (
                         SELECT target_skills.name_skills 
                         FROM skills_userskills target_us
                         JOIN skills_useremail target_ue ON target_us.user_id = target_ue.id
                         JOIN skills_skillsdate target_ssd ON target_us.Skills_id = target_ssd.id
                         JOIN skills_skills target_skills ON target_ssd.skills_id = target_skills.id
                         WHERE target_ue.user_id = :auth_id
                     )""", {"auth_id" : self.request.user.id})# type: ignore
                     return con.fetchall()


@login_required(login_url="/skills/connection") # type: ignore
def create_skills_user(request):
    if request.method == "POST":
        form = SkillsForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.boolean = True
            form.save()
            message = f"Votre {"besoin " if "aide" in form.instance.skills else "compétence "} a bien été enregistré avec succès !"
            messages.success(request, message)
            return redirect("skills:index")
    else:
        form = SkillsForm()
        return render(request, "skills/add_skills.html", {"form": form})
     
          






