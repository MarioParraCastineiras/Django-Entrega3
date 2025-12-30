from rest_framework.routers import DefaultRouter
from .views import SpotifyViewSet

router = DefaultRouter()
router.register(r'spotify', SpotifyViewSet, basename='spotify')

urlpatterns=router.urls