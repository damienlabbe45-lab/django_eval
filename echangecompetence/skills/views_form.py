from asgiref.sync import sync_to_async
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import SkillsForm
from .models import UserSkills, Useremail


@login_required(login_url="/skills/connection")  # type: ignore
async def create_skills_user(request):
    """associate a skill or a need for the current user"""
    if request.method == "POST":
        form = SkillsForm(request.POST)
        is_valid = await sync_to_async(form.is_valid)()
        if is_valid:
            form.instance.boolean = True
            skills = await form.asave()
            current_user = await request.auser()
            user_email = await Useremail.objects.aget(user=current_user)
            await UserSkills.objects.acreate(
                user=user_email,
                skills=skills,
            )
            message = (
                f"Votre {'besoin ' if 'aide' in form.instance.skills.name_skills else 'compétence '}"
                "a bien été enregistré avec succès !"
            )
            messages.success(request, message)
            return redirect("skills:index")
    else:
        form = await sync_to_async(SkillsForm)()

    return await sync_to_async(render)(request, "skills/add_skills.html", {"form": form})