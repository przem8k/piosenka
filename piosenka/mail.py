from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.loader import get_template


def send_new_to_review_mails(item):
    reviewers = [
        user
        for user in User.objects.filter(is_active=True)
        if item.can_be_approved_by(user)
    ]
    subject = "PzT: Nowy materiał czeka na Twoją korektę."
    for reviewer in reviewers:
        if not reviewer.email:
            continue
        context = {"item": item, "reviewer": reviewer, "site": settings.SITE}
        html_content = get_template("mail/new_to_review.html").render(context)
        email = EmailMessage(subject, body=html_content, to=[reviewer.email])
        email.content_subtype = "html"
        email.send()


def send_item_approved_mail(item, approver):
    if not item.author.email:
        return
    subject = "PzT: Materiał został opublikowany."
    context = {"item": item, "approver": approver, "site": settings.SITE}
    html_content = get_template("mail/item_approved.html").render(context)
    email = EmailMessage(subject, body=html_content, to=[item.author.email])
    email.content_subtype = "html"
    email.send()
