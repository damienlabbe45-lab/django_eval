from asgiref.sync import sync_to_async
from django.forms import DateTimeInput, ModelForm
from django.utils import timezone

from .models import SkillsDate

class SkillsForm(ModelForm):
    """class to create skills and needs with the opening hours"""

    class Meta:
        """true class to create the formula of SkillsDate to create """
        model = SkillsDate
        fields = ["skills", "date_begin", "date_before"]
        labels = {
            "skills": "nom de la compétence",
            "date_begin": "à partir de quel jour vous êtes dispo?",
            "date_before": "Jusqu'à quand vous êtes disponible",
        }
        widgets = {
            "date_begin": DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%"
            ),
            "date_before": DateTimeInput(
                            attrs={"type": "datetime-local"},
                            format="%Y-%m-%dT%"
            ),
        }

    def __init__(self, *args, **kwargs):
        """initialize for the sub-class the formula. self.initial in default is the value of date is today."""
        super().__init__(*args, **kwargs)
        if not self.instance.pk and not self.initial.get("date_begin"):
            self.initial["date_begin"] = timezone.now().strftime("%Y-%m-%dT")

        if not self.instance.pk and not self.initial.get("date_before"):
            self.initial["date_before"] = timezone.now().strftime("%Y-%m-%dT")


    async def asave(self, commit:bool = True):
        """sync_to_async convert the synchrone function save  to asynchronous function"""
        return await sync_to_async(self.save)(commit)