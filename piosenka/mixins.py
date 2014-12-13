from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404


class ContentItemViewMixin(object):
    """ Mixin added to default views for displaying the content. Adds information needed to render
    controls (e.g.  if the link to the edit view should be displayed. """
    def get_context_data(self, **kwargs):
        context = super(ContentItemViewMixin, self).get_context_data(**kwargs)
        context['can_edit'] = self.request.user.is_active and (
            self.request.user.is_staff or self.request.user == self.object.author)
        return context


class CheckAuthorshipMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        item = self.get_object()
        if not (self.request.user.is_staff or self.request.user == item.author):
            raise Http404
        return super(CheckAuthorshipMixin, self).dispatch(*args, **kwargs)


class CheckLoginMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CheckLoginMixin, self).dispatch(*args, **kwargs)


class ManageInlineFormsetMixin(object):
    """ requires .get_managed_formset_class() to be defined """
    def get_managed_formset(self):
        cls = self.get_managed_formset_class()
        if self.request.POST:
            return cls(self.request.POST, instance=self.object)
        else:
            return cls(instance=self.object)

    def get_context_data(self, **kwargs):
        context = super(ManageInlineFormsetMixin, self).get_context_data(**kwargs)
        context[self.get_managed_formset_class().model.__name__.lower()] = \
            self.get_managed_formset()
        return context
