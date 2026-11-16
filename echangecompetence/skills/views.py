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


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_skills_date_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return SkillsDate.objects.filter(boolean = False ).order_by("-date_before")[
        :10
    ]