from django.urls import path

from .views import (
    main,
    Individual,
    update_individual,
    list_of_skills,
    skills,
    transition_to_watsapp,
    transition_to_microsoft_teams,
    sending_the_message,
    detailed_skill,
    list_of_working,
    detailed_of_working,
    list_of_projects,
    detailed_of_project,
)

urlpatterns = [
    path('', main),
    path('<int:pk>', Individual.as_view(), name="отобразить личные данные"),
    path('update', update_individual, name="редактировать личные данные"),
    path('1/data/skills', list_of_skills, name="отобразить навыки"),
    path('1/data/skills/<pk>', detailed_skill, name="отобразить конкретный навык"),
    path('1/data/working', list_of_working, name="отобразить рабочие места"),
    path('1/data/working/<pk>', detailed_of_working, name="отобразить конкретное рабочее место"),
    path('1/data/project', list_of_projects, name="отобразить проекты"),
    path('1/data/project/<pk>', detailed_of_project, name="отобразить конкретный проект"),
    path('1/data/all', skills, name="отобразить всё"),
    path('sending_the_message', sending_the_message, name="отправка сообщения с сайта мне"),
    path('watsapp', transition_to_watsapp, name="переход в ВатсАпп"),
    path('microsoft_teams', transition_to_microsoft_teams, name="переход во вражеский мессенджер"),
]
