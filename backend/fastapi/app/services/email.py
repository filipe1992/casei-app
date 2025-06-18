from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.core.config import settings
from pathlib import Path

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent.parent / 'templates/email'
)

async def send_email(email_to: str, subject: str, body: dict, template_name: str = "verification_email.html"):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=body,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message, template_name=template_name)

async def send_verification_email(email_to: str, token: str, name: str):
    subject = "Confirmação de E-mail"
    verification_url = f"{settings.FRONTEND_URL}/confirm-email/{token}"
    body = {
        "title": "Confirme seu e-mail",
        "name": name,
        "verification_url": verification_url
    }
    await send_email(email_to, subject, body, template_name="verification_email.html")

async def send_password_reset_email(email_to: str, token: str, name: str):
    subject = "Redefinição de Senha"
    reset_url = f"{settings.FRONTEND_URL}/reset-password/{token}"
    body = {
        "title": "Redefina sua senha",
        "name": name,
        "reset_url": reset_url
    }
    await send_email(email_to, subject, body, template_name="password_reset_email.html") 