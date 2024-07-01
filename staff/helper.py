import random
import string
from django.core.mail import send_mail
from django.conf import settings




import random
import string

def generate_otp(length=6):
    digits = string.digits
    otp = ''.join(random.choices(digits, k=length))
    return otp

def send_otp_email(email, otp):
    """Send an OTP email using Django's email backend."""
    subject = 'Your OTP Code'
    message = f'Your OTP code is {otp}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    try:
        send_mail(subject, message, email_from, recipient_list)
        return True
    except Exception as e:
        print(e)
        return False
    



def generate_random_string(length=10):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))


