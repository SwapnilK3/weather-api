from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import WeatherData, DataSource
from .serializers import WeatherDataSerializer, DataSourceSerializer
from utils.parsers import get_weather_data
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.shortcuts import render, redirect
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from django.views.generic import TemplateView 
from django.db.models import Count, Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class WeatherDataViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing weather data
    for querying and fetching data from database using following URL:
    http://127.0.0.1:8000/api/weather/?region=UK&parameter=Tmax&year=year&month=month
    
    for fetching data from MetOffice API and storing it in the database go to the following URL:
    http://127.0.0.1:8000/api/weather/fetch_data/
    """
    serializer_class = WeatherDataSerializer
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    
    def get_queryset(self):
        """
        Optionally restricts the returned weather data,
        by filtering against query parameters in the URL.
        """
        queryset = WeatherData.objects.all().order_by('-year', '-month', 'source')
        
        # Apply filters based on query params
        if 'region' in self.request.query_params :
            if self.request.query_params.get('region') != 'all':
                queryset = queryset.filter(source__region=self.request.query_params.get('region'))
            
        if 'parameter' in self.request.query_params :
            if self.request.query_params.get('parameter') != 'all':
                queryset = queryset.filter(source__parameter=self.request.query_params.get('parameter'))
                
        # Date filtering options
        if 'year' in self.request.query_params :
            if self.request.query_params.get('year') != 'all':
                queryset = queryset.filter(year=self.request.query_params.get('year'))
        
        if 'month' in self.request.query_params :
            if self.request.query_params.get('month') != 'all':             
                queryset = queryset.filter(month=self.request.query_params.get('month'))
 
        return queryset            
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        # HTML renderer
        if request.accepted_renderer.format == 'html':
            # Get unique regions and parameters for filters
            regions = DataSource.objects.values_list('region', flat=True).distinct()
            parameters = DataSource.objects.values_list('parameter', flat=True).distinct()
            years = WeatherData.objects.values_list('year', flat=True).distinct().order_by('-year')
            
            # Pagination - 100 records per page
            page = request.GET.get('page', 1)
            paginator = Paginator(queryset, 100)  # Show 100 records per page
            
            try:
                weather_data = paginator.page(page)
            except PageNotAnInteger:
                weather_data = paginator.page(1)
            except EmptyPage:
                weather_data = paginator.page(paginator.num_pages)
            
            context = {
                'weather_data': weather_data,
                'regions': regions,
                'parameters': parameters,
                'years': years,
                'page_obj': weather_data,  # For compatibility with pagination template
                'is_paginated': paginator.num_pages > 1  # Flag to show pagination controls
            }
            return render(request, 'api/view_weather_data.html', context)
        
        # Default JSON response
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
            

    
    
class DataSourceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing data sources read-only
    for adding new data sources go to the following URL:
    http://127.0.0.1:8000/api/source/add_source/
    
    for getting available regions go to the following URL:
    http://127.0.0.1:8000/api/source/get_regions/
    """
    serializer_class = DataSourceSerializer
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    
    def get_queryset(self):
        """
        Optionally restricts the returned data sources,
        by filtering against query parameters in the URL.
        """
        queryset = DataSource.objects.all()
        
        # Apply filters based on query params
        if 'region' in self.request.query_params:
            queryset = queryset.filter(region=self.request.query_params.get('region'))
            
        if 'parameter' in self.request.query_params:
            queryset = queryset.filter(parameter=self.request.query_params.get('parameter'))
            
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        # HTML renderer
        if request.accepted_renderer.format == 'html':
            search_query = request.GET.get('search', '')
            if search_query:
                queryset = queryset.filter(
                    Q(region__icontains=search_query) | 
                    Q(parameter__icontains=search_query)
                )
            
            context = {
                'sources': queryset,
                'search_query': search_query
            }
            return render(request, 'api/view_data_source.html', context)
        
        # Default JSON response
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def get_regions(self, request):
        """
        Endpoint to get a list of available regions
        """
        regions = DataSource.objects.values_list('region', flat=True).distinct()

        return Response({'regions': regions}, template_name='api/view_regions.html')
        
        # For API requests, return JSON
        # return Response(list(regions))
    
    @action(detail=False, methods=['post', 'get'])
    def add_source(self, request):
        """
        Endpoint to add a new data source and fetch data.
        """
        # Handle GET request - render the form
        if request.method == 'GET':
            regions = [
                "UK", "England", "Wales", "Scotland", "Northern_Ireland",
                "England_and_Wales", "England_N", "England_S", "England_E", "England_W", 
                "Scotland_N", "Scotland_E", "Scotland_W"
            ]
            
            parameters = [
                "Tmax", "Tmin", "Tmean", "Rainfall", "Sunshine",
                "Airfrost", "Raindays1mm"
            ]
            
            # Get recent weather data
            weather_data_query = WeatherData.objects.select_related('source').order_by('-year', '-month')
            
            # Apply filters if provided
            selected_region = request.GET.get('region')
            if selected_region:
                weather_data_query = weather_data_query.filter(source__region=selected_region)
            
            selected_parameter = request.GET.get('parameter')
            if selected_parameter:
                weather_data_query = weather_data_query.filter(source__parameter=selected_parameter)
                
            # Get available filter options from database
            available_regions = DataSource.objects.values_list('region', flat=True).distinct()
            available_parameters = DataSource.objects.values_list('parameter', flat=True).distinct()
            
            # Get the first 100 records
            weather_data = weather_data_query[:100]
            
            context = {
                'regions': regions,
                'parameters': parameters,
                'order_options': ['date', 'ranked'],
                'weather_data': weather_data,
                'selected_region': selected_region,
                'selected_parameter': selected_parameter,
                'available_regions': available_regions,
                'available_parameters': available_parameters,
            }
            
            return render(request, 'api/add_data_source.html', context)
        
        if request.method == 'POST':
            region = request.data.get('region')
            parameter = request.data.get('parameter')
            order = request.data.get('order')
            
            url = f"https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/{parameter}/{order}/{region}.txt"
            
            try:
                data_source, created = DataSource.objects.get_or_create(
                region=region, 
                parameter=parameter, 
                order_statistic=order
                )
            
                if not created:
                    # return Response(
                    #     f"Data source for {region} - {parameter} - {order} already exists. Using existing source."
                    # )
                    messages.error(request, f"Data source for {region} - {parameter} - {order} already exists. Using existing source.", extra_tags='alert alert-danger')
                    return redirect('api:datasource-add-source')
                
                
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
                messages.success(request, f"Successfully processed data. Added {created_count} new records.")
                return redirect('api:datasource-list')
                
                # return Response({
                #     "message": f"Successfully processed data. Added {created_count} new records.",
                #     "region": region,
                #     "parameter": parameter
                # }, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                return Response({
                    "error": str(e),
                    "message": "Failed to fetch or process data"
                }, status=status.HTTP_400_BAD_REQUEST)

class HomeView(TemplateView):
    template_name = 'api/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_source_count'] = DataSource.objects.count()
        context['region_count'] = DataSource.objects.values('region').distinct().count()
        context['weather_data_count'] = WeatherData.objects.count()
        context['recent_data'] = WeatherData.objects.order_by('-year', '-month')[:8]
        return context


class ApiDocumentationView(TemplateView):
    template_name = 'api/api_docs.html'
    