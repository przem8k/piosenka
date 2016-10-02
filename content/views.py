import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, RedirectView
from django.views.generic.edit import CreateView, UpdateView

from piosenka.mail import send_item_approved_mail
from piosenka.mail import send_new_to_review_mails

_action_logger = logging.getLogger('actions')


class ViewContentView(DetailView):
    """Adds information needed to render controls (e.g. if the link to the edit
    view should be displayed.

    Limits access to the view to authenticated users if not live yet.

    Requirements for impl:
     - self.get_object() has to return the content item
    """

    def dispatch(self, *args, **kwargs):
        if not self.get_object().can_be_seen_by(self.request.user):
            raise Http404
        return super().dispatch(*args, **kwargs)


class AddContentView(CreateView):

    def get_object(self):
        return None

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.object = None
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        ret = super().form_valid(form)
        try:
            send_new_to_review_mails(form.instance)
        except Exception:
            pass
        messages.add_message(self.request, messages.INFO,
                             'Materiał dodany, oczekuje na korektę.')
        _action_logger.info('%s added %s' % (self.request.user, form.instance))
        return ret


class EditContentView(UpdateView):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        item = self.get_object()
        self.object = item
        if not item.can_be_edited_by(self.request.user):
            raise Http404
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        ret = super().form_valid(form)
        _action_logger.info('%s edited %s' % (self.request.user, form.instance))
        return ret


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
                                 'Materiał został już wcześniej zatwierdzony.')
            return item.get_absolute_url()

        if not item.can_be_approved_by(self.request.user):
            messages.add_message(self.request, messages.INFO,
                                 'Ten materiał nie może być zatwierdzony przez '
                                 'Ciebie.')
            return item.get_absolute_url()

        messages.add_message(self.request, messages.INFO,
                             'Edytuj lub zatwierdź materiał przy pomocy linków '
                             'na dole strony.')
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
        if item.is_live():
            messages.add_message(self.request, messages.INFO,
                                 'Materiał został już wcześniej zatwierdzony.')
            return item.get_absolute_url()

        item.reviewed = True
        item.save()
        messages.add_message(self.request, messages.INFO,
                             'Materiał zatwierdzony.')
        _action_logger.info('%s approved %s' % (self.request.user, item))
        try:
            send_item_approved_mail(item, self.request.user)
        except Exception:
            pass
        return item.get_absolute_url()
