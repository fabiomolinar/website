from django.utils import timezone

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.conf import settings
from django.forms.models import model_to_dict

from ali.models import Search

def index(request):
    respose = redirect('search')
    return respose

def search(request):
    return render(request, 'ali/search.html')

def run_search(request):
    # Check if it is an Ajax request and a POST request
    if not request.is_ajax():
        return HttpResponseForbidden("Only Ajax calls are permitted.")
    if not request.method == 'POST':
        return HttpResponseForbidden("Only POST requests are permitted.")
    text_to_search = request.POST.get('text', None)
    if not text_to_search:
        return HttpResponseBadRequest("Missing attributes.")
    
    # Check if the same search has been done in the last few days (set by ALI_SEARCH_CACHE setting)
    query = Search.objects.filter(search_text=text_to_search).order_by('-date_created')
    if query.count() != 0:
        last_entry = query[0]
        days_to_cache = settings.ALI_SEARCH_CACHE
        time_diff = timezone.now() - last_entry.date_created
        if time_diff.days <= days_to_cache:
            return JsonResponse(model_to_dict(last_entry))


    # If not, send request to Scrapyd to get the data

    # Listen to results from the DB
    return JsonResponse({'response':text_to_search})