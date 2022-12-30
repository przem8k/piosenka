from django.urls import re_path

import piosenka.inspect

urlpatterns = [
    re_path(
        r"^permissions$",
        piosenka.inspect.InspectPermissions.as_view(),
        name="inspect_permissions",
    ),
]
