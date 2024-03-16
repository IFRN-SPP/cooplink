from django.urls import path
from .views import *

# Adicione suas URLs aqui
urlpatterns = [
    path("", index, name="index"),
]