from django.urls import path

from .views import main, Individual, update_individual, skills

urlpatterns = [
    path('', main),
    path('<int:pk>', Individual.as_view(), name="отобразить личные данные"),
    path('update', update_individual, name="редактировать личные данные"),
    path('1/data/skills', skills, name="отобразить навыки"),
]
