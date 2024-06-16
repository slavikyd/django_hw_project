"""Url parsing module."""
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dot_app.urls')),
]

urlpatterns += staticfiles_urlpatterns()
