from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings

from .utils import create_signed_url


@shared_task
def send_verification_mail(email: str , full_name:str):

    verification_link = create_signed_url(email)

    context = {
        "verification_link": verification_link,
        "year": timezone.now().year,
        "user": {
            "full_name": full_name  
        }
    }

    cache.set(f"{email}_verification", verification_link, 1500)


    html_content = render_to_string("verification-mail.html", context)

    email_message = EmailMessage(
        subject="Verify Your Email Address",
        body=html_content,
        to=[email],
    )
    email_message.content_subtype = "html"  
    email_message.send()



@shared_task
def send_otp(email: str, otp: int):
    subject = 'Your OTP Code'
    message = f'Your one-time password (OTP) is: {otp}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)