# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^(.+)/$', 'voters.views.ConstituencyView', name='constituency'),
)
