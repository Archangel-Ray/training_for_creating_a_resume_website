from django.shortcuts import redirect
from django.contrib.contenttypes.models import ContentType

from .models import Feedback
from .forms import FeedbackForm


class FeedbackMixin:
    """
    Миксин работает и с ListView, и с DetailView. Добавляет
    блок откликов как к конкретному объекту, так и к спискам.
    """

    feedback_model = Feedback
    feedback_form_class = FeedbackForm

    def get_feedback_content_type(self):
        """Возвращает номер модели к которой привязан этот объект или модель."""
        if hasattr(self, "object"):  # если объект, то для DetailView
            return ContentType.objects.get_for_model(self.object)
        return ContentType.objects.get_for_model(self.model)  # если не объект, то для ListView

    def get_feedback_object_id(self):
        """Возвращает идентификатор объекта для DetailView, или None для ListView"""
        if hasattr(self, "object"):
            return self.object.id
        return None

    def get_feedback_queryset(self):
        """
        Отбирает и возвращает все отзывы для текущего объекта
        или раздела соответственно с пометкой "публиковать".
        """
        return self.feedback_model.objects.filter(
            content_type=self.get_feedback_content_type(),
            object_id=self.get_feedback_object_id(),
            status="published",
        )

    def get_feedback_form(self, data=None):
        """
        Возвращает форму (пустую или с данными)
        и текущего пользователя (для идентификации в форме).
        """
        return self.feedback_form_class(data, user=self.request.user)

    def handle_valid_form(self, form):
        """
        Сохранение отзыва.
        Привязка происходит к текущей модели, в случае если есть идентификатор
        объекта, то к этому объекту. Если объекта нет, то только к модели.
        Если пользователь прошёл аутентификацию, то он сохраняется в отклик,
        иначе сохраняется только имя, если оно было введено.
        И перегружается страница.
        """
        fb = form.save(commit=False)
        fb.content_type = self.get_feedback_content_type()
        fb.object_id = self.get_feedback_object_id()
        if self.request.user.is_authenticated:
            fb.author_user = self.request.user
        fb.save()
        return redirect(self.request.path)

    def post(self, request, *args, **kwargs):
        """Обработка POST-запроса."""
        if hasattr(self, "get_object"):  # сохраняет объект для DetailView
            self.object = self.get_object()
        else:  # сохраняет список для ListView
            self.object_list = self.get_queryset()

        form = self.get_feedback_form(request.POST)  # получает форму

        if form.is_valid():  # сохраняет отклик, если форма без ошибок
            return self.handle_valid_form(form)

        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        """Добавляет в контекст список откликов и форму."""
        context = super().get_context_data(**kwargs)
        context["feedbacks"] = self.get_feedback_queryset()
        context["feedback_form"] = kwargs.get("form", self.get_feedback_form())
        return context
