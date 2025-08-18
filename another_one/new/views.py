from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import F
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    DetailView,
    ListView,
)
from django.views.generic.edit import UpdateView

from new.forms import UpdateIndividualForm
from new.models import (
    MyUser,
    Skill,
    Working,
    Project,
    Course,
)


class GetContext:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['i_am'] = MyUser.objects.get(id=1)
        return context


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


class ListOfSkills(GetContext, ListView):
    template_name = "new/list_of_skills.html"
    model = Skill
    context_object_name = "skills"


list_of_skills = ListOfSkills.as_view()


class DetailedSkill(GetContext, DetailView):
    template_name = "new/detailed_of_skill.html"
    model = Skill
    context_object_name = "skill"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = Skill.objects.exclude(pk=self.object.pk)
        return context


detailed_skill = DetailedSkill.as_view()


class ListOfWorking(GetContext, ListView):
    template_name = "new/list_of_working.html"
    model = Working
    context_object_name = "workings"

    def get_queryset(self):
        queryset = Working.objects.order_by(F('end_date').desc(nulls_first=True))
        return queryset


list_of_working = ListOfWorking.as_view()


class DetailedOfWorking(GetContext, DetailView):
    template_name = "new/detailed_of_working.html"
    model = Working
    context_object_name = "working"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = Working.objects.exclude(pk=self.object.pk)
        return context


detailed_of_working = DetailedOfWorking.as_view()


class ListOfProjects(GetContext, ListView):
    template_name = "new/list_of_projects.html"
    model = Project
    context_object_name = "projects"

    def get_queryset(self):
        queryset = Project.objects.order_by(F('end_date').desc(nulls_first=True))
        return queryset


list_of_projects = ListOfProjects.as_view()


class DetailedOfProject(GetContext, DetailView):
    template_name = "new/detailed_of_project.html"
    model = Project
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = Project.objects.exclude(pk=self.object.pk)
        return context


detailed_of_project = DetailedOfProject.as_view()


class ListOfCourses(GetContext, ListView):
    template_name = "new/list_of_courses.html"
    model = Course
    context_object_name = "courses"

    def get_queryset(self):
        queryset = Course.objects.order_by(F('end_date').desc(nulls_first=True))
        return queryset


list_of_courses = ListOfCourses.as_view()


def skills(request):
    context = {
        "i_am": MyUser.objects.get(id=1),
    }
    return render(request, 'new/display_data.html', context=context)


def transition_to_watsapp(request):
    return redirect("https://wa.me/79885173602")


def transition_to_microsoft_teams(request):
    return redirect("https://teams.microsoft.com/l/chat/0/0?users=sergey.savelyev2020@gmail.com")


def sending_the_message(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        subject = f'Новое сообщение от {name}'
        full_message = f'От: {email}\n\n{message}'

        send_mail(
            subject,
            full_message,
            email,  # от кого
            ['skillfactory_training@mail.ru'],  # кому
            fail_silently=False,
        )
        return render(request, 'new/sending_the_message.html', context={'sent': True})
    return render(request, 'new/sending_the_message.html')
