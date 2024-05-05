from api import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"members", views.MemberViewSet, basename="member")


urlpatterns = [
    path("", include(router.urls)),
    path("login/", views.LoginView.as_view(), name="login"),
    path("", views.birthdays_of_the_day, name="birthdays_of_the_day"),
]
