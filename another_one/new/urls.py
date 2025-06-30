from django.urls import path

from .views import main, Individual, skills

urlpatterns = [
    path('', main),
    path('<int:pk>', Individual.as_view(), name="отобразить личные данные"),
    path('1/data/skills', skills, name="отобразить навыки"),
]
