import datetime

from django.core.urlresolvers import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.dates import MonthArchiveView, DateDetailView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.template import RequestContext, loader
from django.utils.text import slugify
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, Http404
from django.shortcuts import get_object_or_404

from unidecode import unidecode

from artists.models import Artist, Band
from events.models import Event, Venue
from events.forms import EventForm

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
    VENUE_COUNT = 10
    def get_context_data(self, **kwargs):
        context = super(EventIndex, self).get_context_data(**kwargs)
        from django.db.models import Count
        context['popular_venues'] = Venue.objects.all() \
                                                 .annotate(event_count=Count('event')) \
                                                 .order_by('-event_count')[:EventIndex.VENUE_COUNT]
        return context


class EventMonthArchive(MonthArchiveView):
    model = Event
    context_object_name = "events"
    template_name = "events/event_month_archive.html"
    date_field = "datetime"
    month_format = "%m"
    allow_future = True
    allow_empty = True

class AddEvent(CreateView):
    model = Event
    form_class = EventForm
    template_name = "events/add_edit_event.html"
    success_url = reverse_lazy('event_index')

    def form_valid(self, form):
        venue = form.cleaned_data['venue']
        venue.save()
        form.instance.venue = venue
        form.instance.datetime = datetime.datetime.combine(form.cleaned_data['date'],
                                                           form.cleaned_data['time'])
        form.instance.slug = slugify(unidecode(form.cleaned_data['name']))
        form.instance.author = self.request.user
        return super(AddEvent, self).form_valid(form)

class EditEvent(UpdateView):
    model = Event
    form_class = EventForm
    template_name = "events/add_edit_event.html"
    success_url = reverse_lazy('event_index')

    date_field = "datetime"
    month_format = "%m"
    allow_future = True

    def get_initial(self):
        return {
            'date': self.object.datetime,
            'time': self.object.datetime,
            'venue': self.object.venue,
            'description_trevor': self.object.description_trevor,
        }

    def form_valid(self, form):
        venue = form.cleaned_data['venue']
        venue.save()
        form.instance.venue = venue
        form.instance.datetime = datetime.datetime.combine(form.cleaned_data['date'],
                                                           form.cleaned_data['time'])
        form.instance.slug = slugify(unidecode(form.cleaned_data['name']))
        form.instance.pk = self.object.pk
        return super(EditEvent, self).form_valid(form)
