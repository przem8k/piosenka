import time
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import RedirectView, TemplateView
from django.views.generic.edit import (CreateView, DeleteView, FormView,
                                       UpdateView)

from content.trevor import put_text_in_trevor
from content.views import (AddContentView, ApproveContentView, EditContentView,
                           ReviewContentView, ViewContentView)
from events.forms import ExternalEventForm
from events.models import ExternalEvent, Performer, get_events_for


class EventIndex(TemplateView):
    template_name = "events/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = get_events_for(self.request.user)
        context["performers"] = Performer.objects.filter(
            fb_page_id__isnull=False
        ).exclude(fb_page_id="")
        return context


class AddExternalEvent(LoginRequiredMixin, CreateView):
    model = ExternalEvent
    form_class = ExternalEventForm
    template_name = "events/add_edit_external_event.html"

    def get_success_url(self):
        return reverse("event_index")


class EditExternalEvent(LoginRequiredMixin, UpdateView):
    model = ExternalEvent
    form_class = ExternalEventForm
    template_name = "events/add_edit_external_event.html"

    def get_success_url(self):
        return reverse("event_index")


class DeleteExternalEvent(LoginRequiredMixin, DeleteView):
    model = ExternalEvent

    def get_success_url(self):
        return reverse("event_index")
