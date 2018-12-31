"""Celery tasks"""

from __future__ import absolute_import, unicode_literals
from celery import shared_task
from website import settings

from .models import Search

@shared_task
def recurrent_search():
    """Recurrent request to the ali search spider"""

    text_to_search = "purse"
    Search.send_request_to_server(text_to_search, settings.SCRAPYD_HOST)

@shared_task
def test_debug():
    print("a simple test")
