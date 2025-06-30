from django.shortcuts import render
from django.views.generic import DetailView

from new.models import MyUser


def main(request):
    return render(request, 'new/basic_information.html')


class Individual(DetailView):
    model = MyUser
    template_name = "new/individual_information.html"


def skills(request):
    context = {
        "i_am": MyUser.objects.get(id=1),
    }
    return render(request, 'new/display_data.html', context=context)
