from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import UserAPIView, UserViewset

router = DefaultRouter()
router.register(prefix="", viewset=UserViewset, basename="user")

urlpatterns = [
    path("", UserAPIView.as_view()),
]

urlpatterns += router.urls  # type: ignore
