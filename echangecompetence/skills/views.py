from typing import Any
from django.db import connection
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import generic


from .models import SkillsDate, Skills, UserSkills, Useremail
from .forms import SkillsForm
#from .user import create_user



class IndexView(generic.ListView):
    """View for the home page"""
    template_name = "skills/index.html"
    context_object_name = "latest_skills_date_list"

    def get_queryset(self):
        """Return the last ten skills helping."""
        # ce qui va suivre en commentaire permet de savoir comment les données ont été insérés

        # #create_user() fonction qui a servi à créé les utilisateurs directement
        #with open("C:\\Users\\LabbeD\\OneDrive - Facylities Multi Services\\Documents\\evaldjango\\echangecompetence\\data.sql", 'r', encoding='utf-8') as f:
        # on lit le fichier .sql
        #    sql_content = f.read()
            
        #with connection.cursor() as cursor:
        # on éxécute directement les requètes sql sans passer par l'orm qui aurait néccessiter de faire une boucle for alors que
        # là , on en fait pas, ce qui est nettement plus rapide et plus simple pour un dévelopeur python connaissant assez bien le sql.
        #    cursor.executescript(sql_content)
            
        return SkillsDate.objects.filter(boolean = False ,skills__name_skills__contains='aide ').order_by("-date_before")[
        :10
    ]


class AllskillsView(IndexView):
    """View for present the visitor the skills and need"""
    template_name = "skills/all_skills.html"

    def get_queryset(self):
            """Return the skills and need."""
            return Skills.objects.order_by("name_skills")


#le décorateur method_decorator pour que un autre décorateur qui normalement s'applique à une fonction s'applique à une classe 
#et à ses classes filles ou name précise le nom de la fonction. ici en l'occurence dispatch avec login_required
@method_decorator(login_required(login_url="/skills/connection"), name='dispatch' )# type: ignore
class SkillsUserView(IndexView):
    """View for the current user can help the other users"""
    template_name = "skills/search_skills.html"
    
    def get_queryset(self):
        """Returns users whom the current user can help."""
        with connection.cursor() as con:
            # il aurait été possible de utiliser l'orm.  mais ca aurait créé plusieurs requètes assez compliqué . et là on peut 
            # avec le sql faire cela en une seule requète sql. en résumé, la requète sql fait d'abord les jointures de la sous requète sql
            # ou elle prend les compétences de l'utilisateur actuel et les ajoute devant 'aide pour ' ce qui les transforme en besoin.
            # ces besoins sont transmises à la requète sql principale qui a aussi fait ces jointures.  ensuite on sélectionne les 
            # utilisateurs qui ne sont pas l'utilisateur actuel et qui ont besoin des compétences de l'utilisateur actuel.
            # Enfn on ne garde que leur nom d'utilisateur, leur adresse mail et les noms de leurs besoins.  le target_us, et autre est 
            # juste un renommage de table temporaire qui sert à mieux comprendre qui fait quoi pour les personnes qui lisent la requète
            con.execute("""SELECT DICTINCT auth_user.username, skills_useremail.email, skills_skills.name_skills 
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
                WHERE target_ue.user_id = :auth_id)""", {"auth_id" : self.request.user.id})# type: ignore
            return con.fetchall()

class SkillsUserHelpView(SkillsUserView):
    """View for the current user the others users can then help"""
    template_name = "skills/search_help_skills.html"

    def get_queryset(self):
        """Returns users whom the current user can ask for help."""
        with connection.cursor() as con:
            # il aurait été possible de utiliser l'orm.  mais ca aurait créé plusieurs requètes assez compliqué . et là on peut 
            # avec le sql faire cela en une seule requète sql. en résumé, la requète sql fait d'abord les jointures de la sous requète sql
            # ou elle prend les besoins de l'utilisateur actuel et enlève les 1à premiers caractères ce qui les transforme en compétences.
            # ces compétences sont transmises à la requète sql principale qui a aussi fait ces jointures.  ensuite on sélectionne les 
            # utilisateurs qui ne sont pas l'utilisateur actuel et qui ont les compétences l'utilisateur actuel a besoin.
            # Enfn on ne garde que leur nom d'utilisateur, leur adresse mail et les noms de leurs besoins.  le target_us, et autre est 
            # juste un renommage de table temporaire qui sert à mieux comprendre qui fait quoi pour les personnes qui lisent la requète
            con.execute("""SELECT DISTINCT auth_user.username, skills_useremail.email, skills_skills.name_skills 
            FROM skills_userskills 
            JOIN skills_useremail ON skills_userskills.user_id = skills_useremail.id 
            JOIN auth_user ON skills_useremail.user_id = auth_user.id 
            JOIN skills_skillsdate ON skills_userskills.Skills_id = skills_skillsdate.id 
            JOIN skills_skills ON skills_skillsdate.skills_id = skills_skills.id 
            WHERE skills_useremail.user_id != :auth_id 
            AND skills_skills.name_skills IN (
                SELECT SUBSTR(target_skills.name_skills, 11)
                FROM skills_userskills target_us
                JOIN skills_useremail target_ue ON target_us.user_id = target_ue.id
                JOIN skills_skillsdate target_ssd ON target_us.Skills_id = target_ssd.id
                JOIN skills_skills target_skills ON target_ssd.skills_id = target_skills.id
                WHERE target_ue.user_id = :auth_id AND target_skills.name_skills like 'aide pour %%')""", 
                {"auth_id" : self.request.user.id})# type: ignore
            return con.fetchall()


@login_required(login_url="/skills/connection") # type: ignore
def create_skills_user(request):
    """associate a skill or a need for the current user"""
    if request.method == "POST":
        form = SkillsForm(request.POST)
        if form.is_valid():
            form.instance.boolean = True
            skills = form.save()
            UserSkills.objects.create(
                 user = Useremail.objects.get(user = request.user),
                 Skills = skills)
            message = f"Votre {
                "besoin " if "aide" in form.instance.skills.name_skills else "compétence "} a bien été enregistré avec succès !"
            messages.success(request, message)
            return redirect("skills:index")
    else:
        form = SkillsForm()
        return render(request, "skills/add_skills.html", {"form": form})
          