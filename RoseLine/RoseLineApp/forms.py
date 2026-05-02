from django import forms
from django_select2.forms import Select2Widget
from .models import Horse


class HorseForm(forms.ModelForm):

    class Meta:
        model = Horse
        fields = [
            "name",
            "brand_tag",
            "coat_name",
            "genetics",
            "breed",
            "gender",
            "personality",
            "sire",
            "dam",
            "is_purebred",
            "conceived_date",
            "max_stat",
            "trained",
            "status",
        ]

        widgets = {
            "conceived_date": forms.DateInput(attrs={"type": "date"}),
            "sire": Select2Widget,
            "dam": Select2Widget,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        active_horses = Horse.objects.filter(status=Horse.Status.ACTIVE)

        self.fields["sire"].queryset = active_horses.filter(
            gender=Horse.Gender.MALE
        )

        self.fields["dam"].queryset = active_horses.filter(
            gender=Horse.Gender.FEMALE
        )