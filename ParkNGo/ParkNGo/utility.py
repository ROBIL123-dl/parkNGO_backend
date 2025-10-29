from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

def send_email(user, sentence):
    try:
       
        if not all([settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD]):
            raise ImproperlyConfigured("Email settings are not configured properly.")
        
        
        send_mail(
            subject='Email Verification OTP',
            message=sentence,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return True

    except ImproperlyConfigured as e:
        return False 

    except Exception as e:
        return False
