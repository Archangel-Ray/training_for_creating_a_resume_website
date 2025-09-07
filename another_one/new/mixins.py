from typing import cast

from django.shortcuts import redirect
from django.contrib.contenttypes.models import ContentType
from django.views.generic import ListView

from .models import Feedback
from .forms import FeedbackForm


class FeedbackListMixin:
    """
    Mixin для ListView, чтобы добавить блок откликов ко ВСЕМ объектам списка.
    Пример: общие отзывы о навыках, проектах и т.д.
    """

    feedback_model = Feedback
    feedback_form_class = FeedbackForm

    def get_feedback_content_type(self):
        """Возвращает ContentType для модели списка (например Skill, Project)."""
        return ContentType.objects.get_for_model(self.model)

    def get_feedback_queryset(self):
        """Отзывы без object_id (относятся к разделу в целом)."""
        return self.feedback_model.objects.filter(
            content_type=self.get_feedback_content_type(),
            object_id__isnull=True,
            status="published"
        )

    def get_feedback_form(self, data=None):
        """Возвращает форму (пустую или с данными)."""
        return self.feedback_form_class(data)

    def post(self, request, *args, **kwargs):
        """Обработка отправки отклика."""
        self.object_list = self.get_queryset()
        form = self.get_feedback_form(request.POST)

        if form.is_valid():
            fb = form.save(commit=False)
            fb.content_type = self.get_feedback_content_type()
            fb.object_id = None
            if request.user.is_authenticated:
                fb.author_user = request.user
            fb.save()
            return redirect(request.path)

        # если форма невалидна рендерим с ошибками
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedbacks"] = self.get_feedback_queryset()
        context["feedback_form"] = kwargs.get("form", self.get_feedback_form())
        return context
