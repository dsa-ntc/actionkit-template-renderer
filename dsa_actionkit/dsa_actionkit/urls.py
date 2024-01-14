"""dsa_actionkit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, re_path
from mydsa.views import (
    event_api_moveon_fake,
    event_search_results,
    index,
    login_context,
    logout,
    user_password_forgot,
)
from settings import STATIC_ROOT

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r"^context", login_context),
    re_path(r"^progress", login_context, name="progress"),
    re_path(r"^logout", logout, name="logout"),
    re_path(r"^(?P<name>[-.\w]+)?(/(?P<page>[-.\w]+))?$", index),
    re_path(r"^forgot/$", user_password_forgot, name="user_password_forgot"),
    re_path(
        r"^cms/event/(?P<page>[-.\w]+)/search_results/",
        event_search_results,
        name="event_search_results",
    ),
    re_path(r"^fake/api/events", event_api_moveon_fake, name="event_api_moveon_fake"),
    re_path(r"^fake/stub/reverse", event_api_moveon_fake, name="reverse_donation"),
]

if STATIC_ROOT:
    urlpatterns = staticfiles_urlpatterns()
