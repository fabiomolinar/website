from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden
from django.conf import settings
from django.forms.models import model_to_dict
from django.utils.translation import gettext as _

from ali.models import Search
from ali.models import Tracker
from ali.models import Throttler

def index(request):
    respose = redirect('ali:search')
    return respose

def search(request):
    return render(request, 'ali/search.html')

def tracker(request):
    search_text = Tracker.objects.get_current_search()
    return render(request, 'ali/tracker.html', {'search_text': search_text})

standard_fields_to_client = [
    'average', 'average_nc', 'currency', 'date_created', 'max_price', 'max_price_nc',
    'median', 'median_nc', 'min_price', 'min_price_nc', 'stddev', 'stddev_nc'
]
search_fields_to_client = standard_fields_to_client + ['results', 'number_points', 'number_points_nc']

# API
def get_tracker(request):
    text_to_search = request.POST.get('search_text', None)
    data = {
        'search_text': text_to_search,
        'count': 0,
        'data': []
    }
    query = Search.objects.filter(search_text=text_to_search)
    count = query.count()
    if count != 0:
        data['data'] = list(query.order_by('-id').values(*standard_fields_to_client)[:60])
        data['count'] = count
    return JsonResponse({'data': data})

def run_search(request):
    text_to_search = request.POST.get('text', None)
    session_ip = get_client_ip(request)
    session_id = 'no session id'
    if request.session.session_key:
        session_id = request.session.session_key
    request_ok, failure_message = request_is_valid(request, text_to_search)
    if not request_ok:
        return HttpResponseBadRequest(failure_message)
    # Check if not old entry exists
    exist_current, current = Search.objects.exists_current(search_text=text_to_search, days_to_check=settings.ALI_SEARCH_CACHE)
    if exist_current:
        return JsonResponse(model_to_dict(current, fields=search_fields_to_client))
    # Check if need to throttle user
    accesses_in_last_hour = Throttler.objects.accesses_in_last_hour(session_ip, session_id)
    if accesses_in_last_hour > 3:
        return HttpResponseForbidden(_("Too many requests within an hour"))
    accesses_in_last_24h = Throttler.objects.accesses_in_last_24h(session_ip, session_id)
    if accesses_in_last_24h > 10:
        return HttpResponseForbidden(_("Too many requests within last 24 hours"))
    # Make HTTP request to scrapy server
    request_sent = Search.send_request_to_server(search_text=text_to_search, host=settings.SCRAPYD_HOST)
    if not request_sent:
        return HttpResponseServerError(_("Collector server error"))
    # Update Throttler
    t = Throttler(ip=session_ip, session_id=session_id)
    t.save()
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
        return JsonResponse(model_to_dict(last_entry, fields=search_fields_to_client))
    return HttpResponseServerError(_("No results found"))

# Utils 
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def request_is_valid(request, payload):
    """Checks if the request for data is valid

    Args:
        request: the HTTP request
        payload: the data contained in the request

    Returns:
        (True, "") if the request is valid, (False, message with the reason) otherwise
    """
    # Check if it is an Ajax request and a POST request
    if not request.is_ajax():
        return False, _("Only Ajax calls are permitted")
    if not request.method == 'POST':
        return False, _("Only POST requests are permistted")
    if not payload:
        return False, _("No text to search provided")
    if not isinstance(payload, str):
        return False, _("Invalid search object")
    return True, ""