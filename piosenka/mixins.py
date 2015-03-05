from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404

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
        return super(ContentItemViewMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ContentItemViewMixin, self).get_context_data(**kwargs)
        context['can_edit'] = self.object.can_be_edited_by(self.request.user)
        context['can_approve'] = \
            self.object.can_be_approved_by(self.request.user)
        return context


class ContentItemApproveMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        item = self.get_object()
        if not item.can_be_approved_by(self.request.user):
            raise Http404
        return super(ContentItemApproveMixin, self).dispatch(*args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        item = self.get_object()
        item.reviewed = True
        item.save()
        return item.get_absolute_url()


class CheckAuthorshipMixin(object):
    # TODO this should become ContentItemEditMixin?
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        item = self.get_object()
        if not (self.request.user.is_staff or self.request.user == item.author):
            raise Http404
        return super(CheckAuthorshipMixin, self).dispatch(*args, **kwargs)


class CheckLoginMixin(object):
    # TODO this should become ContentItemAddMixin?
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CheckLoginMixin, self).dispatch(*args, **kwargs)


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
        context = super(ManageInlineFormsetMixin,
                        self).get_context_data(**kwargs)
        context[self.get_managed_formset_class().model.__name__.lower()] = \
            self.get_managed_formset()
        return context
