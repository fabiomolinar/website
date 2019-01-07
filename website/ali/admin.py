"""Ali Admin"""

from django.contrib import admin
from .models import Search
from .models import Tracker
from .models import Throttler

class SearchAdmin(admin.ModelAdmin):
    """Search Model"""
    date_hierarchy = 'date_created'
    list_display = ('search_text', 'results', 'currency', 'min_price', 'median', 'max_price', 'date_created')

class TrackerAdmin(admin.ModelAdmin):
    """Tracker Model"""
    date_hierarchy = 'date_created'
    list_display = ('search_text', 'date_created')

class ThrottlerAdmin(admin.ModelAdmin):
    """Throttler Model"""
    date_hierarchy = 'date_created'
    list_display = ('ip', 'session_id', 'date_created')

admin.site.register(Search, SearchAdmin)
admin.site.register(Tracker, TrackerAdmin)
admin.site.register(Throttler, ThrottlerAdmin)