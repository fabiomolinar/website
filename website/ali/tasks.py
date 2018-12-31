"""Celery tasks"""

from __future__ import absolute_import, unicode_literals
from celery import shared_task
from website import settings

from .models import Search
from .models import Tracker

@shared_task
def tracker_update():
    """Recurrent request to the ali search spider"""

    Search.send_request_to_server(Tracker.objects.get_current_search(), settings.SCRAPYD_HOST)

@shared_task
def test_debug():
    """Debug task for testing"""

    print("a simple test")
