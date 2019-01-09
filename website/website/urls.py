"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
from django.conf.urls.i18n import i18n_patterns

from django.contrib import admin
from django.contrib.sitemaps import views

from zinnia.sitemaps import AuthorSitemap
from zinnia.sitemaps import CategorySitemap
from zinnia.sitemaps import EntrySitemap
from zinnia.sitemaps import TagSitemap

from .sitemaps import StaticViewSitemap

AuthorSitemap.protocol = 'https'
CategorySitemap.protocol = 'https'
EntrySitemap.protocol = 'https'
TagSitemap.protocol = 'https'

sitemaps = {
    'static': StaticViewSitemap,
    'tags': TagSitemap,
    'blog': EntrySitemap,
    'authors': AuthorSitemap,
    'categories': CategorySitemap
}

# URLs witouht Internationalization
urlpatterns = [
    path('sitemap.xml', views.index, {'sitemaps': sitemaps}),
    path('sitemap-<section>.xml', views.sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('i18n/', include('django.conf.urls.i18n')),
]

# URLs with internationalization
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('blog/', include('zinnia.urls')),
    path('comments/', include('django_comments.urls')),
    re_path(r'^', include('base.urls')),
    prefix_default_language=False
)
