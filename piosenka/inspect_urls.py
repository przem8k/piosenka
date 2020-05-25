from django.conf.urls import url

import piosenka.inspect

urlpatterns = [
    url(
        r'^permissions$',
        piosenka.inspect.InspectPermissions.as_view(),
        name='inspect_permissions'),
]
