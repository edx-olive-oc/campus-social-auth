# -*- coding: utf-8 -*-
"""
URLs for campus_social_auth.
"""
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'', TemplateView.as_view(template_name="campus_social_auth/base.html")),
]
