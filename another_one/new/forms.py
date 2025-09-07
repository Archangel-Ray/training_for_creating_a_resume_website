from django.forms import (
    ModelForm,
    DateField,
    DateInput,
    CheckboxSelectMultiple,
    Textarea,
)
# from django.forms.widgets import (
#     FileInput,
# )

from .models import (
    MyUser,
    Feedback,
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
        widgets = {
            # 'photo': FileInput,
            'specialization_professions': CheckboxSelectMultiple,
            'languages': CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['citizenship'].empty_label = '— Не выбрано —'
        self.fields['city'].empty_label = '— Не выбран —'
        self.fields['profession'].empty_label = '— Не выбрана —'
        self.fields['job'].empty_label = '— Не указано —'


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ["author_name", "content"]
        widgets = {
            "content": Textarea(attrs={"rows": 3, "placeholder": "Что Вы думаете об этом..."}),
        }
