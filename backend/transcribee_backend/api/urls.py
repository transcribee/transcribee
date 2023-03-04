from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("documents", views.DocumentViewSet, basename="document")
router.register("users", views.UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
]
