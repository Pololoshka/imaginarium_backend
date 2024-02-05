from rest_framework.routers import DefaultRouter

from . import views as v

router = DefaultRouter()
router.register(prefix="rooms", viewset=v.RoomViewset, basename="rooms")
urlpatterns = router.urls
