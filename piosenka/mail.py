from django.core.mail import EmailMessage
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.contrib.auth.models import User


def send_new_to_review_mails(item, request=None):
    reviewers = [x for x in
                 User.objects.filter(is_staff=True, is_active=True)
                 if x != item.author]
    subject = "PzT: Nowy materiał czeka na Twoją korektę."
    for reviewer in reviewers:
        data = {'item': item, 'reviewer': reviewer}
        context = RequestContext(request, data) if request else Context(data)
        html_content = get_template('mail/new_to_review.html').render(context)
        email = EmailMessage(subject, body=html_content, to=[reviewer.email])
        email.content_subtype = "html"
        email.send()
