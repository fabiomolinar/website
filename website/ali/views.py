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
        
    exist_current, current = Search.objects.exists_current(search_text=text_to_search,days_to_check=settings.ALI_SEARCH_CACHE)
    if exist_current:
        return JsonResponse(model_to_dict(current))

    # If not, send request to Scrapyd to get the data
    url = "http://" + settings.SCRAPYD_HOST + ":6800/schedule.json"
    payload = {
        'project': 'ali',
        'spider': 'search',
        'searchtext': text_to_search
    }
    scrapyd_request = requests.post(url, params=payload)
    if not scrapyd_request.status_code == 200:
        return HttpResponseServerError(_("Collector server error"))
    # DB listener
    db_settings = settings.DATABASES['ali']
    conn = psycopg2.connect(dbname=db_settings['NAME'], 
                            user=db_settings['USER'], 
                            password=db_settings['PASSWORD'], 
                            host=db_settings['HOST'], 
                            port=db_settings['PORT'])
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    curs = conn.cursor()
    curs.execute("LISTEN ali_search;")
    timeout = timezone.now() + timezone.timedelta(0, settings.ALI_SEARCH_TIMEOUT)
    listened = False
    returned_empty = True
    while timezone.now() < timeout:
        time_diff = timeout - timezone.now()
        if select.select([conn], [], [], float(time_diff.seconds)) == ([], [], []):
            listened = False
            timeout = timezone.now()
        else:
            conn.poll()
            while conn.notifies:
                notify = conn.notifies.pop(0)
                if notify.payload == text_to_search:
                    listened = True
                    returned_empty = False
                    timeout = timezone.now()
                elif notify.payload == 'search request returned empty':
                    listened = True
                    returned_empty = True
                    timeout = timezone.now()
    curs.close()
    conn.close()
    if not listened:
        return HttpResponseServerError(_("Collector server timed out"))
    if returned_empty:
        return JsonResponse({'returned_empty': True})
    query = Search.objects.filter(search_text=text_to_search).order_by('-date_created')
    if query.count() != 0:
        last_entry = query[0]
        return JsonResponse(model_to_dict(last_entry))
    return HttpResponseServerError(_("No results found"))