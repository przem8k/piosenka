import os

from django.conf import settings
from django.http import FileResponse


class StaticPageFallbackMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if:
        # 1. It's a 404 (Not Found)
        # 2. The request path ends with a '/' (indicating a directory)
        # 3. An index.html file exists in the corresponding directory
        if response.status_code == 404 and request.path.endswith("/"):

            index_path = os.path.join(
                settings.PZT_STATICPAGE_DIR, request.path.lstrip("/"), "index.html"
            )
            print(index_path)
            if os.path.exists(index_path):
                # Set the Content-Type header for HTML, you may remove this if it is not working in some browser
                response = FileResponse(
                    open(index_path, "rb"), content_type="text/html"
                )
                return response
        elif response.status_code == 404 and request.path.endswith(".json"):
            json_path = os.path.join(
                settings.PZT_STATICPAGE_DIR, request.path.lstrip("/")
            )
            print(json_path)
            if os.path.exists(json_path):
                # Set the Content-Type header for HTML, you may remove this if it is not working in some browser
                response = FileResponse(
                    open(json_path, "rb"), content_type="application/json"
                )
                return response

        return response
