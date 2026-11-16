from django.forms import DateTimeInput, ModelForm
from django.utils import timezone
from .models import SkillsDate

class SkillsForm(ModelForm):
    """classe pour créé les skills avec les horaires"""

    class Meta:
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
        super().__init__(*args, **kwargs)
        # Valeur par défaut : la date actuelle
        if not self.instance.pk and not self.initial.get("date_begin"):
            self.initial["date_begin"] = timezone.now().strftime("%Y-%m-%dT")

        if not self.instance.pk and not self.initial.get("date_before"):
            self.initial["date_before"] = timezone.now().strftime("%Y-%m-%dT")