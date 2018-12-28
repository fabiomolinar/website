import requests
import psycopg2
import psycopg2.extensions
import select

from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from django.conf import settings
from django.forms.models import model_to_dict
from django.utils.translation import gettext as _

from ali.models import Search

def index(request):
    respose = redirect('ali:search')
    return respose

def search(request):
    return render(request, 'ali/search.html')

def run_search(request):
    text_to_search = request.POST.get('text', None)
    request_ok, failure_message = Search.request_is_valid(request, text_to_search)
    if not request_ok:
        return HttpResponseBadRequest(failure_message)
    # Check if not old entry exists
    exist_current, current = Search.objects.exists_current(search_text=text_to_search, days_to_check=settings.ALI_SEARCH_CACHE)
    if exist_current:
        return JsonResponse(model_to_dict(current))
    # Make HTTP request to scrapy server
    request_sent = Search.send_request_to_server(search_text=text_to_search, host=settings.SCRAPYD_HOST)
    if not request_sent:
        return HttpResponseServerError(_("Collector server error"))
    # listen for DB NOTIFY
    listened, returned_empty = Search.objects.listen_for_notify(search_text=text_to_search, search_timeout=settings.ALI_SEARCH_TIMEOUT)
    if not listened:
        return HttpResponseServerError(_("Collector server timed out"))
    if returned_empty:
        return JsonResponse({'returned_empty': True})    
    # HTTP request to scrapy server is done and listened to DB NOTIFY, then we just need to get the latest result
    query = Search.objects.filter(search_text=text_to_search).order_by('-date_created')
    if query.count() != 0:
        last_entry = query[0]
        return JsonResponse(model_to_dict(last_entry))
    return HttpResponseServerError(_("No results found"))