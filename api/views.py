from django.http import HttpResponse


def index():
    return HttpResponse("API: Something goes here")
