# -*- coding: utf-8 -*-
from django.views.generic import DetailView, TemplateView
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, Http404
from django.shortcuts import get_object_or_404

from artists.models import Artist, Band
from events.models import Event, Venue

class VenueView(DetailView):
    model = Venue
    context_object_name = "venue"
    template_name = "events/venue.html"
