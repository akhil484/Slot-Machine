from django.urls import re_path, path
from . import views
from base.views import slot_machine, spin_machine, sign_up, logout_view, login_view, home

urlpatterns = [
    path("", views.home, name='home'),
    path("play/", views.slot_machine, name='slot_machine'),
    path("accounts/login", views.login_view, name='login_view'),
    path("sign_up/", views.sign_up, name='sign_up'),
    path("logout", views.logout_view, name='logout_view'),
    path("ajax-spin-machine/", views.spin_machine, name='spin_machine'),
]