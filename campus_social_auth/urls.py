# -*- coding: utf-8 -*-
"""
URLs for campus_social_auth.
"""
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from .views import HintUsernameView


urlpatterns = [
    url(r'^hint_username_details', HintUsernameView.as_view()),
]
