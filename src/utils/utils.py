# Python
import os
from pprint import pprint
import emails
import jwt
from datetime import datetime, timedelta
from pathlib import Path, WindowsPath
from typing import Optional, Tuple
from emails.template import JinjaTemplate
import tempfile

# Pydantic
from pydantic import BaseModel, UUID4

# SqlAlchemy
from sqlalchemy.orm import class_mapper

# FastAPI
from fastapi import BackgroundTasks

# Pyjwt
from jwt.exceptions import InvalidTokenError

# src utilities
from src.config import settings


def send_email(email_to: str, subject_template="", html_template="", environment={}):
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)


def send_email_attachment(email_to: str, subject_template="", html_template="", filename="", attachment=None, environment={}, attachments=[], filenames=[]):
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    if attachment:
        message.attach(data=open(attachment, 'rb'), filename=filename)
    if attachments:
        for attachment, filename in zip(attachments, filenames):
            message.attach(data=open(attachment, 'rb'), filename=filename)
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)


def send_test_email(email_to: str):
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    template_str = open_html_by_environment("test_email.html")
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": settings.PROJECT_NAME, "email": email_to},
    )


def send_reset_password_email(email_to: str, username: str, token: str, background_tasks: BackgroundTasks = None):
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {username}"
    template_str = open_html_by_environment("reset_password.html")
    if hasattr(token, "decode"):
        use_token = token.decode()
    else:
        use_token = token
    server_host = settings.SERVER_HOST
    frontend_url = "settings.FRONTEND_VALIDATION_URL"
    link = f"{frontend_url}/auth/recover/{token}"
    background_tasks.add_task(
        send_email,
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "email": email_to,
            "token": use_token,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


def send_new_account_email(
        email_to: str, username: str, token: str, background_tasks: BackgroundTasks = None
):
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    template_str = open_html_by_environment("new_account.html")
    if hasattr(token, "decode"):
        use_token = token.decode()
    else:
        use_token = token
    server_host = settings.SERVER_HOST
    frontend_url = settings.FRONTEND_VALIDATION_URL
    link = f"{frontend_url}/auth/activate/{use_token}"
    background_tasks.add_task(
        send_email,
        email_to,
        subject,
        template_str,
        {
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "email": email_to,
            "link": link,
        },
    )


def send_new_account_email_activation_pwd(
    email_to: str, username: str, code: str, password: str, background_tasks: BackgroundTasks = None, first: bool = False
):
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    template_str = open_html_by_environment("new_activation_pwd.html")

    server_host = settings.SERVER_HOST
    frontend_url = 'nada'
    link = f"{frontend_url}/auth/activate?login=true&first={first}"
    environment = {
        "project_name": project_name,
        "username": username,
        "email": email_to,
        "link": link,
        "password": password,
        "code": code,
    }
    background_tasks.add_task(send_email, email_to,
                              subject, template_str, environment)


def send_new_account_email_pwd(
        email_to: str,
        username: str,
        password: str,
        background_tasks: BackgroundTasks = None,
):
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    template_str = open_html_by_environment("new_account_pwd.html")
    background_tasks.add_task(
        send_email,
        email_to,
        subject,
        template_str,
        {
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "email": email_to,
            "password": password,
        },
    )


def send_new_reservation_email(email_to: str, username: str, reservation: BaseModel, token: str, profile_id: UUID4, user_email: str):
    template = open_html_by_environment("approve_reservation.html")
    front_url = settings.FRONTEND_VALIDATION_URL
    if hasattr(token, "decode"):
        use_token = token.decode()
    else:
        use_token = token
    link_approval = f"{front_url}/reservation/approve/{reservation.id}?token={use_token}&approval=Aprobada&traveler_id={profile_id}"
    link_reject = f"{front_url}/reservation/approve/{reservation.id}?token={use_token}&approval=Rechazada&traveler_id={profile_id}"
    send_email(
        email_to=email_to,
        subject_template="New reservation",
        html_template=template,
        environment={"user": username, "email": user_email, "link_approval": link_approval,
                     "link_reject": link_reject, **reservation.dict()},
    )


def send_new_mail_in_reason(email_to: str, username: str, enterprise: BaseModel, reason: BaseModel, dk_number: str):
    template = open_html_by_environment("new_reason.html")
    pprint(enterprise.dict())
    pprint(reason.dict())
    send_email(
        email_to=email_to,
        subject_template="New mail in reason",
        html_template=template,
        environment={"user": username, "email": "email", **
                     enterprise.dict(), **reason.dict(), "dk_number": dk_number},
    )


def send_new_passport_visa_reminder(email_to: str, username: str, document: BaseModel, type: str):
    template = open_html_by_environment(
        "reminder_passport.html") if type == "passport" else open_html_by_environment("reminder_visa.html")
    send_email(
        email_to=email_to,
        subject_template="New reminder",
        html_template=template,
        environment={"user": username, "email": "email", **document.dict(), },
    )


def send_new_mail_in_agreement(email_to: str, username: str, enterprise: BaseModel, agreement: BaseModel, file: None):
    template = open_html_by_environment("new_agreement.html")
    send_email_attachment(
        email_to=email_to,
        subject_template="New agreement",
        html_template=template,
        filename="Acuerdo.pdf",
        attachment=file,
        environment={"user": username, "email": "email",
                     **enterprise.dict(), **agreement.dict()},
    )


def send_new_mail_in_calendar(email_to: str, reservation: BaseModel, files: None, name: str, filenames: list[str]):
    template = open_html_by_environment("new_calendar.html")
    send_email_attachment(
        email_to=email_to,
        subject_template="New Reservation",
        html_template=template,
        filenames=filenames,
        attachments=files,
        environment={"name": name, "email": "email", **reservation.dict()},
    )


def send_new_mail_with_ics(email_to: str, username: str, enterprise: BaseModel, file: None):
    template = open_html_by_environment("approve_reservation.html")
    send_email_attachment(
        email_to=email_to,
        subject_template="New reservation",
        html_template=template,
        filename="Reserva",
        attachment=file,
        environment={"user": username, "email": "email", **enterprise.dict()},
    )


def generate_token(email, action, claims=None):
    delta = timedelta(days=10)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    claims = claims or {}
    encoded_jwt = jwt.encode(
        {
            "exp": exp,
            "nbf": now,
            "action": action,
            "email": email,
            "claims": claims,
        },
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_token(token, action) -> Optional[Tuple]:
    try:
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"])
        assert decoded_token["action"] in action
        return decoded_token["email"], decoded_token["action"]
    except InvalidTokenError:
        return None


def open_html_by_environment(html_name):
    relative_path = Path("src/email/templates")
    if isinstance(relative_path, WindowsPath):
        relative_path = relative_path.as_posix()
    if settings.ENVIRONMENT == "production":
        template_str = open(f"{relative_path}/{html_name}").read()
    else:
        template_str = open(f"{relative_path}/{html_name}").read()
    return template_str


def get_time_zone():
    return "America/Mexico_City"


def object_to_dict(obj, found=None):
    if found is None:
        found = set()
    mapper = class_mapper(obj.__class__)
    columns = [column.key for column in mapper.columns]

    def get_key_value(c): return (c, getattr(obj, c).isoformat()) if isinstance(getattr(obj, c), datetime) else (
        c, getattr(obj, c))
    out = dict(map(get_key_value, columns))
    for name, relation in mapper.relationships.items():
        if relation not in found:
            found.add(relation)
            related_obj = getattr(obj, name)
            if related_obj is not None:
                if relation.uselist:
                    out[name] = [object_to_dict(child, found)
                                 for child in related_obj]
                else:
                    out[name] = object_to_dict(related_obj, found)
    return out
