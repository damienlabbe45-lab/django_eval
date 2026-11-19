from asgiref.sync import sync_to_async
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from typing import override

from .views import IndexView


#le décorateur method_decorator pour que un autre décorateur qui normalement s'applique à une fonction s'applique à une classe 
#et à ses classes filles ou name précise le nom de la fonction. ici en l'occurence dispatch avec login_required
@method_decorator(login_required(login_url="/skills/connection"), name='dispatch' )# type: ignore
class SkillsUserView(IndexView):
    """View for the current user can help the other users"""
    template_name = "skills/search_skills.html"

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
                """SELECT DISTINCT auth_user.username, skills_useremail.email, skills_skills.name_skills
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
                    WHERE target_ue.user_id = :auth_id)""",
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
                """SELECT DISTINCT auth_user.username, skills_useremail.email, skills_skills.name_skills
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
                {"auth_id": auth_id},
            )
            return con.fetchall()