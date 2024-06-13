from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    re_path("app/", include("base.urls")),
    re_path("admin/", admin.site.urls),
]