from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import Feedback


@receiver(post_save, sender=Feedback)
def notify_new_feedback(sender, instance: Feedback, created, **kwargs):
    """Отправка оповещения при добавлении или редактировании отзыва."""
    subject = "Отзыв на моём сайте"
    message = f"""
    от: {instance.created_at}
    Автор: {instance.display_author()}
    Модель: {instance.content_type}
    Объект: {instance.target}
    Сообщение:
    {instance.content}
    """

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,  # от кого
        settings.ADMINS,  # кому
        fail_silently=True,  # чтобы не падало при ошибке
    )
