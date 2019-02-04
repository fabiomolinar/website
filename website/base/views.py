from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden
from django.conf import settings
from django.utils.translation import gettext as _

from ali.models import Throttler
from base.projects.twitter.mentions import TwitterMentions

# Create your views here.

def index(request):
    return render(request, 'base/index.html')

def projects(request):
    return render(request, 'base/projects.html')

def about(request):
    return render(request, 'base/about.html')

def contact(request):
    return render(request, 'base/contact.html')

def view_twitter_mentions(request):
    return render(request, 'base/twitter_mentions.html')

def run_twitter_mentions(request):
    text_to_search = request.POST.get('text', None)
    if text_to_search[0:1] == "@":
        text_to_search = text_to_search[1:len(text_to_search)]
    session_ip = get_client_ip(request)
    session_id = 'no session id'
    if request.session.session_key:
        session_id = request.session.session_key
    request_ok, failure_message = request_is_valid(request, text_to_search)
    if not request_ok:
        return HttpResponseBadRequest(failure_message)
    # Check if need to throttle user
    accesses_in_last_hour = Throttler.objects.accesses_in_last_hour(session_ip, session_id)
    if accesses_in_last_hour > 3:
        return HttpResponseForbidden(_("Too many requests within an hour"))
    accesses_in_last_24h = Throttler.objects.accesses_in_last_24h(session_ip, session_id)
    if accesses_in_last_24h > 10:
        return HttpResponseForbidden(_("Too many requests within last 24 hours"))
    # Make HTTPS request to Twitter API
    tm = TwitterMentions(text_to_search)
    if not tm.get_tweets():
        return HttpResponseServerError(tm.request_message)
    if not settings.DEBUG:
        t = Throttler(ip=session_ip, session_id=session_id)
        t.save()
    if len(tm.mentions) == 0:
        return HttpResponseBadRequest(_("No data found for this account."))
    return JsonResponse({"data": tm.mentions})
    
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

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip