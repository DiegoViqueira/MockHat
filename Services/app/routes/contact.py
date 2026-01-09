"""Contact"""
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from fastapi import APIRouter, HTTPException, status

from app.core.settings import settings
from app.models.email_schema import EmailSchema

router = APIRouter(prefix='/contact', tags=["Contact"])


def verify_recaptcha(token: str) -> bool:
    """Verify the recaptcha token."""
    secret_key = settings.email.CAPTCHA_PRIVATE_KEY
    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data={"secret": secret_key, "response": token}
    )
    result = response.json()
    return result.get("success", False)


def send_email(email_data: EmailSchema):
    """Send an email."""
    try:

        if not verify_recaptcha(email_data.recaptchaToken):
            raise HTTPException(status_code=400, detail="reCAPTCHA no válido")

        sender_email = settings.email.MAIL_USER_INFO
        receiver_email = ["diego.viqueira@mockhat.com",
                          "juanbautista.garcia@mockhat.com"]
        password = settings.email.MAIL_PASS_INFO

        msg = MIMEMultipart()
        msg['From'] = email_data.email
        msg['To'] = ", ".join(receiver_email)
        msg['Subject'] = f"[MOCKHAT] Mensaje de {email_data.name}: {email_data.subject}"

        body = MIMEText(email_data.message, 'plain', 'utf-8')
        msg.attach(body)

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())

    except smtplib.SMTPAuthenticationError as e:
        logging.error("Error de autenticación: %s", e)
        raise HTTPException(
            status_code=500, detail="Error sending email") from e

    except smtplib.SMTPException as e:
        logging.error("Error al enviar el correo: %s", e)
        raise HTTPException(
            status_code=500, detail="Error sending email") from e

    except Exception as e:
        logging.error("Error al enviar el correo: %s", e)
        raise HTTPException(
            status_code=500, detail="Error sending email") from e


@router.post("/send-email", status_code=status.HTTP_200_OK,
             responses={
                 500: {"description": "Internal server error"},
             })
async def send_email_endpoint(email_data: EmailSchema):
    """Send an email."""
    send_email(email_data)
    return {"message": "Correo enviado correctamente"}
