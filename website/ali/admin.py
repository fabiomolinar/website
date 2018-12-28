from django.contrib import admin
from .models import Search

class SearchAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_created'
    list_display = ('search_text','results','currency','min_price','median','max_price','date_created')

admin.site.register(Search, SearchAdmin)