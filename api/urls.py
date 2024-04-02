from api import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"members", views.MemberViewSet, basename="member")


urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("", include(router.urls)),
]
