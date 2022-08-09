from config.settings.base import EMAIL_HOST_USER
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_email(data):
    subject = 'Smart Email'
    # html_message = render_to_string(
    #     'auth/activate.html', {'url': data['url'], 'firstname': data['firstname'], 'lastname': data['lastname'], 'text': data['text']})
    message = ('Subject here')
    # plain_message = strip_tags(message1)
    from_email = EMAIL_HOST_USER
    to = data['to_email']
    # send_mail(subject=data['email_subject'],message=data['email_body'],from_email=EMAIL_HOST_USER,recipient_list=[data['to_email']])
    mail.send_mail(subject, message, from_email,
                   [to])

