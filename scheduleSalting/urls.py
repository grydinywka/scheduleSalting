"""scheduleSalting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin

from schedule.views import SaltingAddView, SaltingEditView, SaltingChangeStatus, SaltingHistory, ReminderEditView

urlpatterns = patterns('',
    url(r'^$', 'schedule.views.salting_list', name="home"),
    url(r'^salting/history/$', SaltingHistory.as_view(), name="salting_history"),

    # url(r'^salting/add/$', 'schedule.views.salting_add', name="salting_add"),
    url(r'^salting/add/$', SaltingAddView.as_view(), name="salting_add"),

    # url(r'^salting/(?P<sid>\d+)/edit/$', 'schedule.views.salting_edit', name="salting_edit"),
    url(r'^salting/(?P<sid>\d+)/edit/$', SaltingEditView.as_view(), name="salting_edit"),

    url(r'^salting/(?P<sid>\d+)/change_status/$', SaltingChangeStatus.as_view(), name="salting_change_status"),

    # reminder edit url
    url(r'^reminder/(?P<rid>\d+)/edit/$', ReminderEditView.as_view(), name="reminder_edit"),

    url(r'^admin/', include(admin.site.urls)),
)
