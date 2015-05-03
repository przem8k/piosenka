from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.generic import RedirectView

from piosenka.mail import send_item_approved_mail


class ReviewContentView(RedirectView):
    """ Redirects to content to be reviewed and puts up a helper message
    depending on whether the item has already been reviewed and whether the user
    has the rights to approve it.

    Requirements for impl:
     - self.get_object() has to return the content item
    """
    permanent = False

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        item = self.get_object()
        if item.is_live():
            messages.add_message(self.request, messages.INFO,
                                 "Materiał został już wcześniej zatwierdzony.")
            return item.get_absolute_url()

        if not item.can_be_approved_by(self.request.user):
            messages.add_message(self.request, messages.INFO,
                                 "Ten materiał nie może być zatwierdzony przez "
                                 "Ciebie.")
            return item.get_absolute_url()

        messages.add_message(self.request, messages.INFO,
                             "Edytuj lub zatwierdź materiał przy pomocy linków "
                             "na dole strony.")
        return item.get_absolute_url()


class ApproveContentView(RedirectView):
    """ Marks the content item as reviewed.

    Requirements for impl:
     - self.get_object() has to return the content item
    """
    permanent = False

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        item = self.get_object()
        if not item.can_be_approved_by(self.request.user):
            raise Http404
        return super().dispatch(*args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        item = self.get_object()
        item.reviewed = True
        item.save()
        messages.add_message(self.request, messages.INFO,
                             "Materiał zatwierdzony.")
        try:
            send_item_approved_mail(item, self.request.user)
        except Exception:
            pass
        return item.get_absolute_url()
