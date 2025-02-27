import pytest
from django.utils import timezone
from api.models import DataSource, WeatherData

@pytest.mark.django_db
class TestDataSource:
    def test_create_data_source(self):
        """Test creating a data source"""
        source = DataSource.objects.create(
            region="UK",
            parameter="Tmax",
            order_statistic="date"
        )
        assert source.id is not None
        assert source.region == "UK"
        assert source.parameter == "Tmax"
        assert source.order_statistic == "date"
    
    def test_data_source_str(self):
        """Test the string representation of a data source"""
        source = DataSource.objects.create(
            region="UK",
            parameter="Tmax",
            order_statistic="date"
        )
        expected = "UK - Tmax - date"
        assert str(source) == expected

@pytest.mark.django_db
class TestWeatherData:
    @pytest.fixture
    def data_source(self):
        return DataSource.objects.create(
            region="UK",
            parameter="Tmax",
            order_statistic="date"
        )
    
    def test_create_weather_data(self, data_source):
        """Test creating weather data"""
        weather = WeatherData.objects.create(
            source=data_source,
            year=2022,
            month=6,
            value=21.5
        )
        assert weather.id is not None
        assert weather.year == 2022
        assert weather.month == 6
        assert weather.value == 21.5
        assert weather.source == data_source