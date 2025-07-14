from django.forms import (
    ModelForm,
    DateField,
    DateInput,
)

from .models import (
    MyUser,
)


class UpdateIndividualForm(ModelForm):
    birthday = DateField(
        widget=DateInput(
            attrs={'type': 'date'},
            format='%Y-%m-%d'
        ),
        required=False,
        label="День рождения"
    )

    class Meta:
        model = MyUser
        fields = [
            "first_name",
            "patronymic",
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
            "languages",
            "motto",
            "about_me",
        ]
