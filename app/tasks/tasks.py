import smtplib

from pydantic import EmailStr

from app.config import settings
from app.tasks.celeryy import celery
from PIL import Image
from pathlib import Path

from app.tasks.email_templates import create_booking_confirmation_template


@celery.task
def process_pic(
    path: str,
):
    im_path = Path(path)
    im = Image.open(im_path)
    miniature = im.resize((200, 100))
    miniature.save(f"app/static/images/miniature_{im_path.name}")


@celery.task
def send_booking_confirmation_email(
    booking: dict,
    email_to: EmailStr,
):
    msg_content = create_booking_confirmation_template(booking, email_to)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
