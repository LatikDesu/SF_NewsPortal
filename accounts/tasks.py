import uuid
from datetime import timedelta

from django.utils.timezone import now

from accounts.models import Author, EmailVerification


def send_email_verification(user_id):
    user = Author.objects.get(id=user_id)
    expiration = now() + timedelta(hours=48)
    record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
    record.send_verification_email()
