class ContentItemViewMixin(object):
    """ Mixin added to default views for displaying the content. Adds information needed to render
    controls (e.g.  if the link to the edit view should be displayed. """
    def get_context_data(self, **kwargs):
        context = super(ContentItemViewMixin, self).get_context_data(**kwargs)
        context['can_edit'] = self.request.user.is_active and (
            self.request.user.is_staff or self.request.user == self.object.author)
        return context
