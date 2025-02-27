import pytest
from django.urls import reverse
from api.models import DataSource, WeatherData

@pytest.mark.django_db
class TestHomeView:
    @pytest.fixture
    def data_source(self):
        return DataSource.objects.create(
            region="UK",
            parameter="Tmax",
            order_statistic="date"
        )
    
    def test_home_view(self, client, data_source):
        """Test the home page loads"""
        url = reverse('api:home')
        response = client.get(url)
        
        assert response.status_code == 200

@pytest.mark.django_db
class TestDataSourceViews:
    def test_add_source_get(self, client):
        """Test the add source form loads correctly"""
        # Fix the URL name to match what's in your urls.py
        url = reverse('api:datasource-add-source')  # Note the hyphen, not underscore
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'regions' in response.context
        assert 'parameters' in response.context
        assert 'order_options' in response.context