from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WeatherDataViewSet, DataSourceViewSet, HomeView, ApiDocumentationView

app_name = 'api'

router = DefaultRouter()
router.register(r'weather', WeatherDataViewSet, basename='weatherdata')
router.register(r'source', DataSourceViewSet, basename='datasource')


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('', include(router.urls)),
    path('docs/', ApiDocumentationView.as_view(), name='docs')
]