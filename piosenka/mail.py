from django.core.mail import EmailMessage
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth.models import User


def send_new_to_review_mails(item):
    reviewers = [x for x in
                 User.objects.filter(is_staff=True, is_active=True)
                 if x != item.author]
    subject = "PzT: Nowy materiał czeka na Twoją korektę."
    for reviewer in reviewers:
        if not reviewer.email:
            continue
        context = Context({'item': item,
                           'reviewer': reviewer,
                           'site': settings.SITE})
        html_content = get_template('mail/new_to_review.html').render(context)
        email = EmailMessage(subject, body=html_content, to=[reviewer.email])
        email.content_subtype = "html"
        email.send()


def send_item_approved_mail(item, approver):
    if not item.author.email:
        return
    subject = "PzT: Materiał został opublikowany."
    context = Context({'item': item,
                       'approver': approver,
                       'site': settings.SITE})
    html_content = get_template('mail/item_approved.html').render(context)
    email = EmailMessage(subject, body=html_content, to=[item.author.email])
    email.content_subtype = "html"
    email.send()


def send_invitation_mail(invitation):
    subject = "PzT: Zaproszenie."
    context = Context({'invitation': invitation})
    html_content = get_template('mail/invitation.html').render(context)
    email = EmailMessage(subject, body=html_content,
                         to=[invitation.email_address])
    email.content_subtype = "html"
    email.send()
