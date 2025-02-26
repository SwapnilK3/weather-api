# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WeatherDataViewSet, DataSourceViewSet

router = DefaultRouter()
router.register(r'weather', WeatherDataViewSet, basename='weatherdata')
router.register(r'source', DataSourceViewSet, basename='datasource')

urlpatterns = [
    path('', include(router.urls)),
]