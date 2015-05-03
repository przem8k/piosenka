from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import RedirectView


class ReviewContentView(RedirectView):
    """ Redirects to content to be reviewed and puts up a helper message
    depending on whether the item has already been reviewed and whether the user
    has the rights to approve it.

    Requirements for impl:
     - self.get_object() has to return the content item
    """

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
