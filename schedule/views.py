from django.shortcuts import render
from django.http import HttpResponse

def salting_list(request):
    return render(request, 'schedule/index.html', {})

