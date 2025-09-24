from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import Feedback, MyUser


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


@receiver(post_delete, sender=MyUser)
def delete_file_on_object_delete(sender, instance, **kwargs):
    """Удаление личной фотографии если пользователь выбирает "Очистить"."""
    if instance.photo:
        instance.photo.delete(save=False)


@receiver(pre_save, sender=MyUser)
def delete_old_file_on_change(sender, instance, **kwargs):
    """Удаление личной фотографии если пользователь меняет её на другую."""
    if not instance.pk:
        return False

    try:
        old_file = MyUser.objects.get(pk=instance.pk).photo
    except MyUser.DoesNotExist:
        return False

    new_file = instance.photo
    if old_file and old_file != new_file:
        old_file.delete(save=False)
