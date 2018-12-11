from django.shortcuts import render
from django.urls import reverse

# Create your views here.

def index(request):
    return render(request, 'base/index.html')

def projects(request):
    return render(request, 'base/projects.html')

def about(request):
    return render(request, 'base/about.html')

def contact(request):
    return render(request, 'base/contact.html')