from django.shortcuts import render
from django.http import HttpResponse
from .models import Salting
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def salting_list(request):
    allSalt = Salting.objects.all()

    paginator = Paginator(allSalt, 3)
    page = request.GET.get('page')
    try:
        allSalt = paginator.page(page)
    except PageNotAnInteger:
        allSalt = paginator.page(1)
    except EmptyPage:
        allSalt = paginator.page(paginator.num_pages)
    return render(request, "schedule/salting.html", {'allSalt': allSalt})

def salting_add(request):
    return render(request, "schedule/salting_add.html", {})
