# -*- coding: utf-8 -*-
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.dates import MonthArchiveView, DateDetailView
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, Http404
from django.shortcuts import get_object_or_404

from artists.models import Artist, Band
from events.models import Event, Venue

class VenueDetail(DetailView):
    model = Venue
    context_object_name = "venue"
    template_name = "events/venue_detail.html"

    def get_context_data(self, **kwargs):
        context = super(VenueDetail, self).get_context_data(**kwargs)
        context['model_meta'] = Venue._meta
        return context

class EventDetail(DateDetailView):
    model = Event
    context_object_name = "event"
    template_name = "events/event_detail.html"
    date_field = "datetime"
    month_format = "%m"
    allow_future = True

    def get_context_data(self, **kwargs):
        context = super(EventDetail, self).get_context_data(**kwargs)
        context['model_meta'] = Event._meta
        return context

class EventIndex(ListView):
    model = Event
    context_object_name = "events"
    template_name = "events/event_index.html"
    queryset = Event.current.all()


class EventMonthArchive(MonthArchiveView):
    model = Event
    context_object_name = "events"
    template_name = "events/event_month_archive.html"
    date_field = "datetime"
    month_format = "%m"
    allow_future = True
    allow_empty = True
