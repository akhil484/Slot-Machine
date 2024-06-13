from django.urls import re_path

from base.views import slot_machine, spin_machine

urlpatterns = [
    re_path("play", slot_machine),
    re_path("ajax-spin-machine/", spin_machine),
]