from django.core.mail import EmailMessage
from django.template import Context, RequestContext
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
        context = Context({'item': item, 'reviewer': reviewer})
        html_content = get_template('mail/new_to_review.html').render(context)
        email = EmailMessage(subject, body=html_content, to=[reviewer.email])
        email.content_subtype = "html"
        email.send()
