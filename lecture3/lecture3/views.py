from django.http import HttpResponse
from django.shortcuts import render

from . import views


def index(request):
    return HttpResponse("Hello, welcome to my main root page")
