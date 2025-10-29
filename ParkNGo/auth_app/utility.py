import random
from django.core.exceptions import ObjectDoesNotExist
from .models import User
from ParkNGo.utility import send_email


def generate_otp_int():
    return random.randint(1000, 9999)


def signup_email(user_id):
    try:
        user = User.objects.get(id=user_id)

        email_otp = generate_otp_int()
        user.otp = email_otp
        user.save()
        sentence = f"Your OTP for email verification is: {email_otp}"
        success = send_email(user, sentence)
        if success:
            return True
        else:
            return False
    except ObjectDoesNotExist:
        return False
    except Exception as e:
        return False

   