import pytest
from rest_framework.test import APIClient
from api.models import DataSource, WeatherData

@pytest.mark.django_db
class TestWeatherDataAPI:
    @pytest.fixture
    def api_client(self):
        return APIClient()
    
    @pytest.fixture
    def data_source(self):
        return DataSource.objects.create(
            region="UK",
            parameter="Tmax",
            order_statistic="date"
        )
    
    @pytest.fixture
    def weather_data(self, data_source):
        """Create some test weather data"""
        items = []
        for month in range(1, 13):
            items.append(WeatherData.objects.create(
                source=data_source,
                year=2022,
                month=month,
                value=15.0 + month
            ))
        return items
    
    def test_list_weather_data(self, api_client, weather_data):
        """Test listing weather data"""
        url = '/api/weather/'
        response = api_client.get(url, format='json')
        
        assert response.status_code == 200
        assert 'results' in response.data
        # Depending on your pagination, you might need to adjust this
        assert len(response.data['results']) > 0
        
    def test_filter_by_region(self, api_client, data_source, weather_data):
        """Test filtering weather data by region"""
        url = '/api/weather/?region=UK'
        response = api_client.get(url, format='json')
        
        assert response.status_code == 200
        assert len(response.data['results']) == 12
        
        # Test non-existent region
        url = '/api/weather/?region=NonExistent'
        response = api_client.get(url, format='json')
        
        assert response.status_code == 200
        assert len(response.data['results']) == 0
        
    def test_filter_by_year_and_month(self, api_client, weather_data):
        """Test filtering weather data by year and month"""
        url = '/api/weather/?year=2022&month=6'
        response = api_client.get(url, format='json')
        
        assert response.status_code == 200
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['month'] == 6
        assert response.data['results'][0]['year'] == 2022