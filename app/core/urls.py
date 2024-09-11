from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="api/members/")),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("", include("django_prometheus.urls")),
]
