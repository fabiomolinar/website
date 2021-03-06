from django.contrib import sitemaps
from django.urls import reverse

class StaticViewSitemap(sitemaps.Sitemap):
    i18n = True
    protocol = 'https'

    def items(self):
        return [
            'index', 'projects', 'about', 'contact',
            'view_twitter_mentions',
            'zinnia:entry_archive_index', 
            'ali:search', 'ali:tracker'
        ]

    def location(self, item):
        return reverse(item)

    def changefreq(self, item):
        default_freq = 'weekly'
        freqs = {
            'index': 'weekly',
            'projects': 'weekly',
            'zinnia:entry_archive_index': 'daily',
            'about': 'monthly',
            'contact': 'monthly'
        }
        if item in freqs:
            return freqs[item]
        return default_freq

    def priority(self, item):
        default_priority = 0.5
        priorities = {
            'projects': 0.6,
            'zinnia:entry_archive_index': 0.6,
            'about': 0.6,
        }
        if item in priorities:
            return priorities[item]
        return default_priority