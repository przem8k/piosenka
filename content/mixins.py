from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.http import Http404

from piosenka.mail import send_new_to_review_mails

# TODO: Some of these throw 404, some redirect to login - unify.
# TODO: Some of these use standard decorators, other defer to can_be_ABC_by
# methods. Use the latter everywhere to centralize the decisions in ContentItem?


class ContentItemViewMixin(object):
    """ Mixin added to default views for displaying the content.

    Adds information needed to render controls (e.g. if the link to the edit
    view should be displayed.

    Limits access to the view to authenticated users if not live yet."""
    def dispatch(self, *args, **kwargs):
        if not self.get_object().can_be_seen_by(self.request.user):
            raise Http404
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_edit'] = self.object.can_be_edited_by(self.request.user)
        context['can_approve'] = \
            (self.object.can_be_approved_by(self.request.user) and
             not self.object.is_live())
        return context


class ContentItemAddMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        ret = super().form_valid(form)
        try:
            send_new_to_review_mails(form.instance)
        except Exception:
            pass
        messages.add_message(self.request, messages.INFO,
                             "Materiał dodany, oczekuje na korektę.")
        return ret


class ContentItemEditMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        item = self.get_object()
        if not (self.request.user.is_staff or self.request.user == item.author):
            raise Http404
        return super().dispatch(*args, **kwargs)


class CheckStaffMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not (self.request.user.is_staff):
            raise Http404
        return super().dispatch(*args, **kwargs)


class ManageInlineFormsetMixin(object):
    """ requires .get_managed_formset_class() to be defined """
    def get_managed_formset(self):
        cls = self.get_managed_formset_class()
        if self.request.POST:
            return cls(self.request.POST, instance=self.object)
        else:
            return cls(instance=self.object)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.get_managed_formset_class().model.__name__.lower()] = \
            self.get_managed_formset()
        return context
