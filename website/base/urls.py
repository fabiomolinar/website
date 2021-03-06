from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('projects/', views.projects, name='projects'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('projects/twitter-mentions/', views.view_twitter_mentions, name='view_twitter_mentions'),
    path('projects/twitter-mentions/run', views.run_twitter_mentions, name='run_twitter_mentions'),
    path('projects/ali/', include('ali.urls')),
    path('sitemap', views.return_sitemaps),
    path('sitemaps', views.return_sitemaps),
    path('sitemaps.xml', views.return_sitemaps)
]