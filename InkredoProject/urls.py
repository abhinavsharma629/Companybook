from django.contrib import admin
from django.urls import path, include
from Ink.urls import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Ink.urls')),
]