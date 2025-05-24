from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Task

@receiver(pre_save, sender=Task)
def notify_task_status_change(sender, instance, **kwargs):
    if not instance.pk or not instance.owner or not instance.owner.email:
        return

    try:
        previous = Task.objects.get(pk=instance.pk)
    except Task.DoesNotExist:
        return

    if previous.status != instance.status:
        subject = f"Изменён статус задачи: {instance.title}"
        message = (
            f"Здравствуйте, {instance.owner.username}!\n\n"
            f"Статус вашей задачи '{instance.title}' изменился:\n"
            f"Был: {previous.status}\n"
            f"Стал: {instance.status}\n\n"
            "Посмотреть задачу можно в вашем личном кабинете."
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.owner.email],
            fail_silently=False,
        )
