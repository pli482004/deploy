from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, "website/index.html")


def about(request):
    return render(request, "website/about.html")


def select(request):
    return render(request, "website/select.html")