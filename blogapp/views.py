from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def test(req: HttpRequest):
    return HttpResponse('<b>ok</b>')
