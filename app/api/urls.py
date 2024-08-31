from api import views
from django.urls import path, include
from django.conf import settings
from rest_framework.routers import DefaultRouter
from api.apps import ApiConfig


router = DefaultRouter()
router.register(r"members", views.MemberViewSet, basename="member")

app_name = ApiConfig.name

urlpatterns = [
    path("", include(router.urls)),
    path("login/", views.LoginView.as_view(), name="login"),
    path(
        "get-birthdays-of-the-day/",
        views.get_birthdays_of_the_day,
        name="get_birthdays_of_the_day",
    ),
]

if settings.DEBUG == True:
    urlpatterns += [
        path('birthdays_of_the_day_test/', views.birthdays_of_the_day_test, name='birthdays_of_the_day_test'),
    ]
