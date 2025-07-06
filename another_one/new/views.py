from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView

from new.forms import UpdateIndividualForm
from new.models import MyUser


def main(request):
    return render(request, 'new/basic_information.html')


class Individual(DetailView):
    model = MyUser
    template_name = "new/individual_information.html"


class UpdateIndividual(UpdateView):
    model = MyUser
    form_class = UpdateIndividualForm
    template_name = "new/individual_information_update.html"
    success_url = reverse_lazy("редактировать личные данные")

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user


update_individual = UpdateIndividual.as_view()


def skills(request):
    context = {
        "i_am": MyUser.objects.get(id=1),
    }
    return render(request, 'new/display_data.html', context=context)
