from django.urls import path

from .views import dashboard, test

urlpatterns = [
    path("test", test),
]
