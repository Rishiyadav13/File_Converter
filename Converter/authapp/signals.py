from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from authapp.models import User


@receiver(post_save, sender=User)
def mail_sending(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to Our Website!'
        message = f'Hi {instance.first_name},\n\nThank you for registering on our website.'
        from_email = settings.EMAIL_HOST_USER
        to_email = [instance.email]
        send_mail(subject, message, from_email, to_email)
        
