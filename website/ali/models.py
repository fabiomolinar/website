"""Ali App Models

This module contains classes which encapsulate the logic necessary to read search queries results done at AliExpress website using the AliExpress scrapy spider.

"""
from django.db import models
from django.contrib.postgres import fields as postgres_fields
from django.utils.translation import gettext as _
from django.utils import timezone

class SearchManager(models.Manager):
    """Manager with table-wide methods for the general search type results class"""

    def exists_current(self, search_text, days_to_check):
        """Checks if there is an entry for a certain text that is not older than a predefined number of days

        Args:
            search_text: the text to be searched
            days_to_check: how many days old the latest entry can be

        Returns:
            (True, most updated entry) if an entry exists that is not too old, (False, None) otherwise 
        """
        query = self.filter(search_text=search_text).order_by('-date_created')
        if query.count() != 0:
            last_entry = query[0]
            time_diff = timezone.now() - last_entry.date_created
            if time_diff.days <= days_to_check:
                return True, last_entry
        return False, None

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