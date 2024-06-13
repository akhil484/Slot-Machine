from django.urls import re_path

from base.views import slot_machine

urlpatterns = [
    re_path("play/", slot_machine),
]