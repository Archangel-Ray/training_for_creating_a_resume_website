from django.forms import ModelForm

from new.models import MyUser


class UpdateIndividualForm(ModelForm):
    class Meta:
        model = MyUser
        fields = [
            "first_name",
            "last_name",
            "photo",
            "biological_sex",
            "birthday",
            "citizenship",
            "city",
            "profession",
            "specialization_professions",
            "the_level_of_professionalism",
            "job",
            "motto",
            "about_me",
        ]
