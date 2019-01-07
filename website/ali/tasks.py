"""Celery tasks"""

from __future__ import absolute_import, unicode_literals
from celery import shared_task
from website import settings
from django.utils import timezone

from .models import Search
from .models import Tracker
from .models import Throttler

@shared_task
def tracker_update():
    """Recurrent request to the ali search spider"""

    Search.send_request_to_server(Tracker.objects.get_current_search(), settings.SCRAPYD_HOST)

@shared_task
def clean_throttler():
    """Delete old entries to the Throttler DB"""
    tr = timezone.now() - timezone.timedelta(days=2)
    Throttler.filter(date_created__lt=tr).delete()

@shared_task
def test_debug():
    """Debug task for testing"""

    print("a simple test")
