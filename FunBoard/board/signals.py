from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Reaction, News
from django.contrib.auth.models import User
from FunBoard import settings


@receiver(post_save, sender=Reaction)
def new_reaction(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject=f'Отклик на объявление {instance.advertisement.name}',
            message=f'На ваше объявление откликнулись',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.advertisement.author.email],
        )

    if not created:
        if instance.status == 'A':
            message = f'Ваше предложение одобрили'
        elif instance.status == 'R':
            message = f'Ваше предложение отклонили'

        send_mail(
            subject=f'Ваш отклик на объявление {instance.advertisement.name} рассмотрели',
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.advertisement.author.email],
        )


@receiver(post_delete, sender=Reaction)
def del_reaction(sender, instance, using, **kwargs):
    if using:
        send_mail(
            subject=f'Ваш отклик на объявление {instance.advertisement.name} рассмотрели',
            message='Автор объявления был в шоке и удалил ваше предложение',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.advertisement.author.email],
        )


@receiver(post_save, sender=News)
def send_news(sender, instance, created, **kwargs):
    if created:
        emails = []
        emails += [us.email for us in User.objects.all()]
        html_content = render_to_string(
            'mail_news.html',
            {
                'content': instance.content,
            }
        )
        msg = EmailMultiAlternatives(
            subject=f'Важная новость - "{instance.name}"',
            body='',
            from_email='shavnicyn.work@yandex.ru',
            to=emails,
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
