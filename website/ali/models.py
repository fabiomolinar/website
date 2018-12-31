"""Ali App Models

This module contains classes which encapsulate the logic necessary to read
search queries results done at AliExpress website using the AliExpress scrapy spider.

"""
from django.db import models
from django.contrib.postgres import fields as postgres_fields
from django.utils.translation import gettext as _
from django.utils import timezone
from django.conf import settings

class SearchManager(models.Manager):
    """Manager with table-wide methods for the general search type results class"""

    def exists_current(self, search_text, days_to_check):
        """
        Checks if there is an entry for a certain text that is not older than a 
        predefined number of days

        Args:
            search_text: the text to be searched
            days_to_check: how many days old the latest entry can be

        Returns:
            (True, most updated entry) if an entry exists that is not too old, 
            (False, None) otherwise
        """
        query = self.filter(search_text=search_text).order_by('-date_created')
        if query.count() != 0:
            last_entry = query[0]
            time_diff = timezone.now() - last_entry.date_created
            if time_diff.days <= days_to_check:
                return True, last_entry
        return False, None

    def listen_for_notify(self, search_text, search_timeout):
        """
        Listen for notify events on the DB and check if they notify the
        desired text or if the DB notifies an empty search result

        Args:
            search_text: the text to be listening to as payload from NOTIFY
            search_timeout: the listening timeout period

        Returns:
            (False, None) if nothing is listened
            (True, False) if listened for the desired payload
            (True, True) if listened for empty results payload
        """
        import select
        import psycopg2
        import psycopg2.extensions

        from django.conf import settings
        
        db_data = settings.DATABASES['ali']
        listened = None
        returned_empty = None

        conn = psycopg2.connect(dbname=db_data['NAME'], user=db_data['USER'], password=db_data['PASSWORD'], host=db_data['HOST'], port=db_data['PORT'])
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        curs = conn.cursor()
        curs.execute("LISTEN ali_search;")

        timeout = timezone.now() + timezone.timedelta(0, search_timeout)
        while timezone.now() < timeout:
            time_diff = timeout - timezone.now()
            if select.select([conn], [], [], float(time_diff.seconds)) == ([], [], []):
                listened = False
                timeout = timezone.now()
            else:
                conn.poll()
                while conn.notifies:
                    notify = conn.notifies.pop(0)
                    if notify.payload == search_text:
                        listened = True
                        returned_empty = False
                        timeout = timezone.now()
                    if notify.payload == 'search request returned empty':
                        listened = True
                        returned_empty = True
                        timeout = timezone.now()
        curs.close()
        conn.close()
        return listened, returned_empty

class Search(models.Model):
    """Data returned from crawling a search results page from Ali"""

    # manager
    objects = SearchManager()

    # text used on the search
    search_text = models.TextField(verbose_name="text used on the search query")
    # primary fields
    results = models.IntegerField(verbose_name="total amount of items found by the query")
    walled_brands = postgres_fields.ArrayField(models.TextField(verbose_name="name of the highlighted brands"))
    currency = models.CharField(max_length=9)
    # calculated fields
    max_price = models.FloatField(verbose_name="corrected maximum price")
    min_price = models.FloatField(verbose_name="corrected minimum price")
    average = models.FloatField(verbose_name="corrected average price")
    median = models.FloatField(verbose_name="corrected median price")
    stddev = models.FloatField(verbose_name="corrected standard deviation price")
    number_points = models.IntegerField(verbose_name="number of items used on the corrected calculations")
    max_price_nc = models.FloatField(verbose_name="non-corrected maximum price")
    min_price_nc = models.FloatField(verbose_name="non-corrected minimum price")
    average_nc = models.FloatField(verbose_name="non-corrected average price")
    median_nc = models.FloatField(verbose_name="non-corrected median rice")
    stddev_nc = models.FloatField(verbose_name="non-corrected standard deviation price")
    number_points_nc = models.IntegerField(verbose_name="number of items used on the non-corrected calculations")
    # housekeeping fields
    used_url = models.URLField(max_length=1000, verbose_name="URL used to retrieve the data")
    project = models.CharField(max_length=51, verbose_name="name of the Scrapy project")
    spider = models.CharField(max_length=51, verbose_name="name of the Scrapy spider")
    server_name = models.CharField(max_length=51, verbose_name="server name")
    date_created = models.DateTimeField(verbose_name="date the data was collected")

    @classmethod
    def request_is_valid(cls, request, payload):
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

    @classmethod
    def send_request_to_server(cls, search_text, host):
        """Send HTTP POST request to scrapy server

        Args:
            search_text: text to be searched by the search spider
            host: scrapy server host

        Returns:
            True if HTTP response status equals 200, False otherwise
        """
        import requests
        url = "http://" + host + ":6800/schedule.json"
        payload = {
            'project': 'ali',
            'spider': 'search',
            'searchtext': search_text
        }
        scrapyd_request = requests.post(url, params=payload)
        if scrapyd_request.status_code == 200:
            return True
        return False

class TrackerManager(models.Manager):
    """Tracker manager"""

    def get_current_search(self):
        """Function to define which text is to be used for the tracker"""

        text_to_search = "mp3"
        if settings.ALI_DEFAULT_TRACKER:
            text_to_search = settings.ALI_DEFAULT_TRACKER
        # Get new value if one is defined on the DB
        query = self.order_by('-id')
        if query.count() != 0:
            text_to_search = query[0].search_text
        return text_to_search

class Tracker(models.Model):
    """
    DB to keep track of item currently being used to feed the tracker view
    and to store which ones have been used before.
    """

    objects = TrackerManager()

    search_text = models.TextField(verbose_name="text used on the search query")
    date_created = models.DateTimeField(verbose_name="date created", auto_now_add=True)
