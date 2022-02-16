from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from urllib.parse import urljoin


def send_verify(user):
    verify_link = reverse("auth:verify", args=[user.email, user.activation_key])
    subject = "Verify your email"
    message = f"""For verify {user.username} on {settings.DOMAIN_NAME}
    follow this link - {urljoin(settings.DOMAIN_NAME, verify_link)}"""
    send_mail(
        subject,
        message,
        "noreply@localhost",
        [
            user.email,
        ],
    )
