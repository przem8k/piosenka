import locale
import sys

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


class InspectLocale(TemplateView):
    template_name = 'inspect_locale.html'

    @method_decorator(login_required)
    @method_decorator(permission_required('piosenka.inspect',
                                          raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['locale'] = str(locale.getlocale())
        context['default_locale'] = str(locale.getdefaultlocale())
        context['default_locale'] = str(locale.getdefaultlocale())
        context['filesystem_encoding'] = str(sys.getfilesystemencoding())
        context['default_encoding'] = str(sys.getdefaultencoding())
        return context


class InspectPermissions(TemplateView):
    template_name = 'inspect_permissions.html'

    @method_decorator(login_required)
    @method_decorator(permission_required('piosenka.inspect',
                                          raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context
