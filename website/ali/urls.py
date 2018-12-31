from django.urls import path

from . import views

app_name = 'ali'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('run-search', views.run_search, name='run_search'),
    path('tracker/', views.tracker, name='tracker'),
    path('get-tracker', views.get_tracker, name='get_tracker')
]