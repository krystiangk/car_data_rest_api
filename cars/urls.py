from django.urls import path, include
from .views import CarViewSet, RatingViewSet, PopularViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('cars', CarViewSet, basename='cars')
router.register('rate', RatingViewSet, basename='rate')
router.register('popular', PopularViewSet, basename='popular')
urlpatterns = router.urls
