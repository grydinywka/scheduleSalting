from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from .models import Salting
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime

def getDateRemoving(date_salting, required_salting):
    deltaSalting = datetime.timedelta(days=int(required_salting))
    return date_salting + deltaSalting

def salting_list(request):
    allSalt = Salting.objects.all()

    # try to order salting list
    order_by = request.GET.get('order_by', '')
    if order_by in ('date_salting', 'date_removing', 'id'):
        allSalt = allSalt.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            allSalt = allSalt.reverse()
    elif order_by == '':
        allSalt = allSalt.order_by('date_removing')

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
