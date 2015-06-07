from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404


class CheckStaffMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if not (self.request.user.is_staff):
            raise Http404
        return super().dispatch(*args, **kwargs)
