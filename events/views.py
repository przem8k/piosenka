import datetime

from django.core.urlresolvers import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.dates import MonthArchiveView, DateDetailView
from django.views.generic.edit import CreateView, UpdateView
from django.utils.text import slugify
from django.http import Http404

from unidecode import unidecode

from artists.models import Entity
from events.models import EntityPerformance, Event, Venue
from events.forms import EventForm, PerformanceFormSet
from frontpage.trevor import put_text_in_trevor
from frontpage.views import CheckAuthorshipMixin, CheckLoginMixin


class VenueDetail(DetailView):
    model = Venue
    context_object_name = "venue"
    template_name = "events/venue_detail.html"

    def get_context_data(self, **kwargs):
        context = super(VenueDetail, self).get_context_data(**kwargs)
        context['model_meta'] = Venue._meta
        return context


class EntityDetail(DetailView):
    model = Entity
    context_object_name = "entity"
    template_name = "events/entity.html"

    def dispatch(self, *args, **kwargs):
        if not self.get_object().still_plays:
            raise Http404
        return super(EntityDetail, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EntityDetail, self).get_context_data(**kwargs)
        context['events'] = [x.event for x in EntityPerformance.objects.filter(entity=self.object)]
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
        context['can_edit'] = self.request.user.is_active and (
            self.request.user.is_staff or self.request.user == self.object.author)
        return context


def add_context_for_menu(context):
    from django.db.models import Count
    context['popular_venues'] = Venue.objects.all() \
        .annotate(event_count=Count('event')) \
        .order_by('-event_count')[:EventIndex.VENUE_COUNT]
    context['active_entities'] = Entity.objects.all() \
        .annotate(event_count=Count('entityperformance')) \
        .order_by('-event_count')[:EventIndex.ENTITY_COUNT]
    return context


class EventIndex(ListView):
    model = Event
    context_object_name = "events"
    template_name = "events/event_index.html"
    queryset = Event.current.all()
    VENUE_COUNT = 15
    ENTITY_COUNT = 15

    def get_context_data(self, **kwargs):
        context = super(EventIndex, self).get_context_data(**kwargs)
        return add_context_for_menu(context)


class EventMonthArchive(MonthArchiveView):
    model = Event
    context_object_name = "events"
    template_name = "events/event_month_archive.html"
    date_field = "datetime"
    month_format = "%m"
    allow_future = True
    allow_empty = True

    def get_context_data(self, **kwargs):
        context = super(EventMonthArchive, self).get_context_data(**kwargs)
        return add_context_for_menu(context)


class ManagePerformancesMixin(object):
    def get_performances_formset(self):
        if self.request.POST:
            return PerformanceFormSet(self.request.POST, instance=self.object)
        else:
            return PerformanceFormSet(instance=self.object)

    def get_context_data(self, **kwargs):
        context = super(ManagePerformancesMixin, self).get_context_data(**kwargs)
        context['performances'] = self.get_performances_formset()
        return context

    def form_valid(self, form):
        performances = self.get_performances_formset()
        if not performances.is_valid():
            raise RuntimeError()
        performances.instance = form.instance

        ret = super(ManagePerformancesMixin, self).form_valid(form)
        performances.save()
        return ret


class AddEvent(CheckLoginMixin, ManagePerformancesMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = "events/add_edit_event.html"
    success_url = reverse_lazy('event_index')

    def get_initial(self):
        initial_description = "Tutaj opisz wydarzenie. Zaznacz fragment tekstu aby dodać \
            **pogrubienie** albo [odsyłacz](#)."
        return {
            'description_trevor': put_text_in_trevor(initial_description)
        }

    def form_valid(self, form):
        performances = super(AddEvent, self).get_performances_formset()
        if not performances.is_valid():
            return self.form_invalid(form)

        venue = form.cleaned_data['venue']
        venue.save()
        form.instance.venue = venue
        form.instance.datetime = datetime.datetime.combine(form.cleaned_data['date'],
                                                           form.cleaned_data['time'])
        form.instance.slug = slugify(unidecode(form.cleaned_data['name']))
        form.instance.author = self.request.user

        return super(AddEvent, self).form_valid(form)


class EditEvent(CheckAuthorshipMixin, ManagePerformancesMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = "events/add_edit_event.html"

    date_field = "datetime"
    month_format = "%m"
    allow_future = True

    def get_object(self):
        import datetime
        import time
        year = self.kwargs['year']
        month = self.kwargs['month']
        day = self.kwargs['day']
        slug = self.kwargs['slug']
        date_stamp = time.strptime(year+month+day, "%Y%m%d")
        event_date = datetime.date(*date_stamp[:3])
        return Event.objects.get(slug=slug,
                                 datetime__year=event_date.year,
                                 datetime__month=event_date.month,
                                 datetime__day=event_date.day)

    def get_initial(self):
        return {
            'date': self.object.datetime.strftime("%d.%m.%Y"),
            'time': self.object.datetime.strftime("%H:%M"),
            'venue_selection': self.object.venue,
            'description_trevor': self.object.description_trevor,
        }

    def form_valid(self, form):
        performances = super(EditEvent, self).get_performances_formset()
        if not performances.is_valid():
            return self.form_invalid(form)

        venue = form.cleaned_data['venue']
        venue.save()
        form.instance.venue = venue
        form.instance.datetime = datetime.datetime.combine(form.cleaned_data['date'],
                                                           form.cleaned_data['time'])
        return super(EditEvent, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()
