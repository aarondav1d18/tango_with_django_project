from django.shortcuts import render
from django.http import HttpResponse

def index(request) -> HttpResponse:
    return HttpResponse("Rango says hey there partner! Head to the <a href='/rango/about/'>About</a> page.")

def about(request):
    return HttpResponse("Rango says here is the about page. Return to the <a href='/rango/'>Index</a> page.")