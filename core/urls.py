from django.contrib import admin
from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path('', include('app.urls')),
]

if settings.DEBUG:
    urlpatterns += [path('admin/', admin.site.urls)]