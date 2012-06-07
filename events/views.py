# -*- coding: utf-8 -*-
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, Http404
from django.shortcuts import get_object_or_404
from artists.models import Artist, Band
from events.models import Event


