from asgiref.sync import sync_to_async
from django.shortcuts import render
from django.views.generic import ListView
from typing import override


from .models import SkillsDate, Skills
#from .user import create_user

class IndexView(ListView):
    """View for the home page"""
    template_name = "skills/index.html"
    context_object_name = "latest_skills_date_list"

    def _get_items_sync(self):
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
        return list(
            SkillsDate.objects.filter(
                boolean=False,
                skills__is_need=True,
            ).order_by("-date_before")[:10]
        )

    async def get_items(self):
        """convert the synchronous function _get_items_sync(self) to asynchronous function """
        return await sync_to_async(self._get_items_sync)()

    async def get(self, request):
        """fetch the result the function get_items and convert render to asycnhronous function"""
        items = await self.get_items()
        context = {
            self.context_object_name: items,
            "object_list": items,
        }
        return await sync_to_async(render)(request, self.template_name, context)


class AllskillsView(IndexView):
    """View for present the visitor the skills and need"""
    template_name = "skills/all_skills.html"

    @override
    def _get_items_sync(self): 
        """Return the skills and need."""
        return list(Skills.objects.order_by("name_skills"))
          