from django.urls import path

from .views import dashboard, test

urlpatterns = [
    path("", dashboard),
    path("test", test),
]
