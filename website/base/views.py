from django.shortcuts import render
from django.urls import reverse

# Create your views here.

def index(request):
    page_name = {'index':True}
    return render(request, 'base/index.html', {'page_name':page_name})

def projects(request):
    page_name = {'projects':True}
    return render(request, 'base/projects.html', {'page_name':page_name})

def about(request):
    page_name = {'about':True}
    return render(request, 'base/about.html', {'page_name':page_name})

def contact(request):
    page_name = {'contact':True}
    return render(request, 'base/contact.html', {'page_name':page_name})