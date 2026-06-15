from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


def send_email(subject: str, email_to: list[str], html_tempalte, context):
    msg = EmailMultiAlternatives(
        subject=subject,
        from_email="pmayg.surajpur@gmail.com",
        to=email_to
    )
    html_tempalte = get_template(html_tempalte)
    html_alternative = html_tempalte.render(context)
    msg.attach_alternative(html_alternative, "text/html")
    msg.send(fail_silently=False)