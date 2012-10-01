def site_context(request):
    url_segments = [x for x in request.path.split("/") if len(x) > 0]
    section = url_segments[1] if len(url_segments) > 1 else None
    context = {'section': section}
    return context
