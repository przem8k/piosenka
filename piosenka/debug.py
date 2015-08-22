import locale
import sys

from django.http import HttpResponse, Http404


def debug_locale(request):
    if not (request.user.has_perm('piosenka.debug')):
        raise Http404

    info = ["locale: " + str(locale.getlocale()),
            "default locale: " + str(locale.getdefaultlocale()),
            "filesystem encoding: " + str(sys.getfilesystemencoding()),
            "default encoding: " + str(sys.getdefaultencoding())]
    return HttpResponse("<br />".join(info))
