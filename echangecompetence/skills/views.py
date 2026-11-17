from typing import Any

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import SkillsDate
from .forms import SkillsForm
#from .user import create_user
#from django.db import connection


class IndexView(generic.ListView):
    template_name = "skills/index.html"
    context_object_name = "latest_skills_date_list"

    def get_queryset(self):
        """Return the last five published questions."""
        #with open("C:\\Users\\LabbeD\\OneDrive - Facylities Multi Services\\Documents\\evaldjango\\echangecompetence\\data.sql", 'r', encoding='utf-8') as f:
        #    sql_content = f.read()
            
        #with connection.cursor() as cursor:
        #    cursor.executescript(sql_content)
            
        #create_user() fonction qui a servi à créé les utilisateurs directement
        return SkillsDate.objects.filter(boolean = False ).order_by("-date_before")[
        :10
    ]


