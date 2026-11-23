from asgiref.sync import sync_to_async
from django.db import connection
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.views import redirect_to_login
from django.urls import reverse_lazy
from typing import override

from .views import IndexView



class AsyncLoginRequiredMixin(AccessMixin):
    """Asynchronous version of LoginRequiredMixin for views with async get/post."""

    async def handle_no_permission(self):
        '''function for a redirecting URL'''
        return await sync_to_async(redirect_to_login)(
            self.request.get_full_path(), # type: ignore
            self.get_login_url(),
            self.get_redirect_field_name(),
        )

    async def dispatch(self, request, *args, **kwargs):
        """check if a user is connected. if connected, the user goes to the url he wants. else, the user 
        is redirecting to another URL."""
        user = await request.auser()
        if not user.is_authenticated:
            return await self.handle_no_permission()
        return await super().dispatch(request, *args, **kwargs) # type: ignore
    
class SkillsUserView(AsyncLoginRequiredMixin, IndexView):
    """View for the current user can help the other users"""
    template_name = "skills/search_skills.html"
    login_url = reverse_lazy("skills:connection")

    def _fetch_rows(self, auth_id):
        """Returns users whom the current user can help in a SQL request."""
        with connection.cursor() as con:
            # il aurait été possible de utiliser l'orm.  mais ca aurait créé plusieurs requètes assez compliqué . et là on peut 
            # avec le sql faire cela en une seule requète sql. en résumé, la requète sql fait d'abord les jointures de la sous requète sql
            # ou elle prend les compétences de l'utilisateur actuel et les ajoute devant 'aide pour ' ce qui les transforme en besoin.
            # ces besoins sont transmises à la requète sql principale qui a aussi fait ces jointures.  ensuite on sélectionne les 
            # utilisateurs qui ne sont pas l'utilisateur actuel et qui ont besoin des compétences de l'utilisateur actuel.
            # Enfn on ne garde que leur nom d'utilisateur, leur adresse mail et les noms de leurs besoins.  le target_us, et autre est 
            # juste un renommage de table temporaire qui sert à mieux comprendre qui fait quoi pour les personnes qui lisent la requète

            con.execute(
                """SELECT DISTINCT auth_user.username, auth_user.email, "aide pour " || skills_skills.name_skills, date_begin, 
                date_before
                FROM skills_userskills
                JOIN auth_user ON skills_userskills.user = auth_user.id
                JOIN skills_skillsdate ON skills_userskills.skills = skills_skillsdate.id
                JOIN skills_skills ON skills_skillsdate.skills_id = skills_skills.id
                WHERE auth_user.id != :auth_id
                AND is_need = True
                AND boolean = True
                AND EXISTS (
                    SELECT 1
                    FROM skills_userskills target_us
                    JOIN auth_user target_ue ON target_us.user = auth_user.id
                    JOIN skills_skillsdate target_ssd ON target_us.skills = target_ssd.id
                    JOIN skills_skills target_skills ON target_ssd.skills_id = target_skills.id
                    WHERE target_ue.id = :auth_id
                    AND target_skills.name_skills = skills_skills.name_skills
                    AND is_need = False
                )""",
                {"auth_id": auth_id},
            )
            return con.fetchall()

    @override
    async def get_items(self):
        """fetch the user with a asynchronous function and fetch the results of _fetch_rows and transmitted the identifiant of the user"""
        user = await self.request.auser()
        return await sync_to_async(self._fetch_rows)(user.pk)

class SkillsUserHelpView(SkillsUserView):
    """View for the current user the others users can then help"""
    template_name = "skills/search_help_skills.html"

    @override
    def _fetch_rows(self, auth_id):
        """Returns users whom the current user can ask for help."""
        with connection.cursor() as con:
            # il aurait été possible de utiliser l'orm.  mais ca aurait créé plusieurs requètes assez compliqué . et là on peut 
            # avec le sql faire cela en une seule requète sql. en résumé, la requète sql fait d'abord les jointures de la sous requète sql
            # ou elle prend les besoins de l'utilisateur actuel et enlève les 1à premiers caractères ce qui les transforme en compétences.
            # ces compétences sont transmises à la requète sql principale qui a aussi fait ces jointures.  ensuite on sélectionne les 
            # utilisateurs qui ne sont pas l'utilisateur actuel et qui ont les compétences l'utilisateur actuel a besoin.
            # Enfn on ne garde que leur nom d'utilisateur, leur adresse mail et les noms de leurs besoins.  le target_us, et autre est 
            # juste un renommage de table temporaire qui sert à mieux comprendre qui fait quoi pour les personnes qui lisent la requète
            con.execute(
                """SELECT DISTINCT auth_user.username, auth_user.email, skills_skills.name_skills, date_begin, date_before
                FROM skills_userskills
                JOIN auth_user ON skills_userskills.user = auth_user.id
                JOIN skills_skillsdate ON skills_userskills.skills = skills_skillsdate.id
                JOIN skills_skills ON skills_skillsdate.skills_id = skills_skills.id
                WHERE auth_user.id != :auth_id
                AND boolean = True
                AND is_need = False
                AND EXISTS (
                    SELECT 1
                    FROM skills_userskills target_us
                    JOIN auth_user target_ue ON target_us.user = target_ue.id
                    JOIN skills_skillsdate target_ssd ON target_us.skills = target_ssd.id
                    JOIN skills_skills target_skills ON target_ssd.skills_id = target_skills.id
                    WHERE target_ue.id = :auth_id
                    AND is_need = True
                    AND target_skills.name_skills = skills_skills.name_skills
                )""",
                {"auth_id": auth_id},
            )
            return con.fetchall()