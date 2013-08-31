from django.conf.urls.defaults import *
from django.http import HttpResponse
from django.utils import simplejson as json
from django.views.generic.base import View

class JSONSearchIndexMixin(object):  
    def render_to_response(self, context):  
        "Returns a JSON response containing 'context' as payload"  
        return self.get_json_response(self.convert_index_to_json(context["index"]))  
  
    def get_json_response(self, content, **httpresponse_kwargs):  
        "Construct an `HttpResponse` object."  
        return HttpResponse(content,  
                            content_type='application/json',  
                            **httpresponse_kwargs)  
  
    def convert_index_to_json(self, index):  
        "Convert python index object to JSON"  
        return json.dumps(index) 

class ArtistSearchIndex(JSONSearchIndexMixin, View):
    def get(self, request, *args, **kwargs):
        context = {"index": ["678", "123", "ab ab ab"]}
        return self.render_to_response(context)

class SongSearchIndex(JSONSearchIndexMixin, View):
    def get(self, request, *args, **kwargs):
        context = {"index": ["abc", "cde", "fge"]}
        return self.render_to_response(context)

urlpatterns = patterns('',
    url(r'^artists$', ArtistSearchIndex.as_view(), name="search_index_artists"),
    url(r'^songs$', SongSearchIndex.as_view(), name="search_index_songs"),
)
