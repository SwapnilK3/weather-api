from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import WeatherData, DataSource
from .serializers import WeatherDataSerializer, DataSourceSerializer
from utils.parsers import get_weather_data
from rest_framework.viewsets import ReadOnlyModelViewSet

class WeatherDataViewSet(ReadOnlyModelViewSet):
    """
    ViewSet for viewing and editing weather data
    for querying and fetching data from database using following URL:
    http://127.0.0.1:8000/api/weather/?region=UK&parameter=Tmax&year=year&month=month
    
    for fetching data from MetOffice API and storing it in the database go to the following URL:
    http://127.0.0.1:8000/api/weather/fetch_data/
    """
    serializer_class = WeatherDataSerializer
    def get_queryset(self):
        """
        Optionally restricts the returned weather data,
        by filtering against query parameters in the URL.
        """
        queryset = WeatherData.objects.all()
        
        # Apply filters based on query params
        if 'region' in self.request.query_params:
            queryset = queryset.filter(source__region=self.request.query_params.get('region'))
            
        if 'parameter' in self.request.query_params:
            queryset = queryset.filter(source__parameter=self.request.query_params.get('parameter'))
            
        # Date filtering options
        if 'year' in self.request.query_params:
            queryset = queryset.filter(year=self.request.query_params.get('year'))
        
        if 'month' in self.request.query_params:
            queryset = queryset.filter(month=request.query_params.get('month'))
 
        return queryset            
    
    @action(detail=False, methods=['post'])
    def fetch_data(self, request):
        """
        Endpoint to fetch weather data from MetOffice.
        
        Request body parameters:
        - region: Region code (e.g., 'UK', England', 'Scotland', 'Wales', 'England_East', etc.) 
        - parameter: Weather parameter (e.g., 'Tmax', 'Tmin', 'Rainfall', 'Sunshine', etc.)
        - order_statistic: Sort order ('ranked' or 'date')
        
        json example:
        {
            "region": "UK",
            "parameter": "Tmax",
            "order_statistic": "date"
        }
        """
        region = request.data.get('region', 'UK')
        parameter = request.data.get('parameter', 'Tmax')
        order = request.data.get('order', 'date')
        
        url = f"https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/{parameter}/{order}/{region}.txt"
        
        try:
            data_source, created = DataSource.objects.get_or_create(
            region=region, 
            parameter=parameter, 
            order_statistic=order
        )
        
            if not created:
                return Response(
                    f"Data source for {region} - {parameter} - {order} already exists. Using existing source."
                )
            
            
            parsed_data = get_weather_data(url)
            created_count = 0
            
            for item in parsed_data:
                # Skip header or non-data rows
                if not item.get('year') or not item.get('jan'):
                    continue
                    
                year = item.get('year')
                
                # Process each month's data
                for month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 
                              'jul', 'aug', 'sep', 'oct', 'nov', 'dec']:
                    if month in item and item[month] not in ['---', '']:
                        # Convert month name to month number
                        month_num = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 
                                    'may': 5, 'jun': 6, 'jul': 7, 'aug': 8, 
                                    'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}[month]
                        
                        obj, created = WeatherData.objects.update_or_create(
                                year=year,
                                month=month_num,
                                source=data_source,  # Use the data_source object directly
                                defaults={'value': float(item[month])}
                            )
                        
                        if created:
                            created_count += 1
            
            return Response({
                "message": f"Successfully processed data. Added {created_count} new records.",
                "region": region,
                "parameter": parameter
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                "error": str(e),
                "message": "Failed to fetch or process data"
            }, status=status.HTTP_400_BAD_REQUEST)
            
    # @action(detail=False, methods=['get'])
    # def get_data(self, request):
    #     """
    #     Endpoint to get weather data with filtering options
        
    #     Query parameters:
    #     - region: Filter by region (default: UK)
    #     - parameter: Filter by parameter (default: Tmax)
    #     - year: Filter by specific year
    #     - month: Filter by specific month (1-12)
        
        
    #     """
    #     # Initialize queryset with all weather data
    #     queryset = WeatherData.objects.all()
        
    #     # Apply filters based on query params
    #     if 'region' in request.query_params:
    #         queryset = queryset.filter(source__region=request.query_params.get('region'))
            
    #     if 'parameter' in request.query_params:
    #         queryset = queryset.filter(source__parameter=request.query_params.get('parameter'))
            
    #     # Date filtering options
    #     if 'year' in request.query_params:
    #         queryset = queryset.filter(year=request.query_params.get('year'))
                
    #     if 'month' in request.query_params:
    #         queryset = queryset.filter(month=request.query_params.get('month'))
                
    #     # Apply pagination if needed
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
        
    #     # If no pagination, return the full queryset
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
    
    
class DataSourceViewSet(ReadOnlyModelViewSet):
    """
    ViewSet for viewing and editing data sources read-only
    for adding new data sources go to the following URL:
    http://127.0.0.1:8000/api/source/add_source/
    
    for getting available regions go to the following URL:
    http://127.0.0.1:8000/api/source/get_regions/
    """
    queryset = DataSource.objects.all()
    serializer_class = DataSourceSerializer
    
    @action(detail=False, methods=['get'])
    def get_regions(self, request):
        """
        Endpoint to get a list of available regions
        """
        regions = DataSource.objects.values_list('region', flat=True).distinct()
        return Response(regions)
    
    @action(detail=False, methods=['post'])
    def add_source(self, request):
        """
        Endpoint to fetch weather data from MetOffice.
        
        Request body parameters:
        - region: Region code (e.g., 'UK', England', 'Scotland', 'Wales', 'England_East', etc.) 
        - parameter: Weather parameter (e.g., 'Tmax', 'Tmin', 'Rainfall', 'Sunshine', etc.)
        - order: Sort order ('ranked' or 'date')
        
        json example:
        {
            "region": "UK",
            "parameter": "Tmax",
            "order": "date"
        }
        """
        region = request.data.get('region', 'UK')
        parameter = request.data.get('parameter', 'Tmax')
        order = request.data.get('order', 'date')
        
        url = f"https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/{parameter}/{order}/{region}.txt"
        
        try:
            data_source, created = DataSource.objects.get_or_create(
            region=region, 
            parameter=parameter, 
            order_statistic=order
        )
        
            if not created:
                return Response(
                    f"Data source for {region} - {parameter} - {order} already exists. Using existing source."
                )
            
            
            parsed_data = get_weather_data(url)
            created_count = 0
            
            for item in parsed_data:
                # Skip header or non-data rows
                if not item.get('year') or not item.get('jan'):
                    continue
                    
                year = item.get('year')
                
                # Process each month's data
                for month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 
                              'jul', 'aug', 'sep', 'oct', 'nov', 'dec']:
                    if month in item and item[month] not in ['---', '']:
                        # Convert month name to month number
                        month_num = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 
                                    'may': 5, 'jun': 6, 'jul': 7, 'aug': 8, 
                                    'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}[month]
                        
                        obj, created = WeatherData.objects.update_or_create(
                                year=year,
                                month=month_num,
                                source=data_source,  # Use the data_source object directly
                                defaults={'value': float(item[month])}
                            )
                        
                        if created:
                            created_count += 1
            
            return Response({
                "message": f"Successfully processed data. Added {created_count} new records.",
                "region": region,
                "parameter": parameter
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                "error": str(e),
                "message": "Failed to fetch or process data"
            }, status=status.HTTP_400_BAD_REQUEST)
    