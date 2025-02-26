import requests
from datetime import datetime
from django.core.management.base import BaseCommand
from api.models import WeatherData, DataSource
from utils.parsers import get_weather_data

class Command(BaseCommand):
    help = 'Fetch and parse weather data from UK MetOffice'

    def add_arguments(self, parser):
        parser.add_argument('--region', type=str, default='UK', help='Region to fetch data for')
        parser.add_argument('--parameter', type=str, default='Tmax', help='Parameter to fetch (Tmax, Tmin, etc)')
        parser.add_argument('--order', type=str, default='date', help='order to fetch (ranked, date, etc)')

    def handle(self, *args, **options):
        region = options['region']
        parameter = options['parameter']
        order = options['order']
        url = f"https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/{parameter}/{order}/{region}.txt"
        
        # Check if data source exists, create if not
        data_source, created = DataSource.objects.get_or_create(
            region=region, 
            parameter=parameter, 
            order_statistic=order
        )
        
        if not created:
            self.stdout.write(self.style.WARNING(
                f"Data source for {region} - {parameter} - {order} already exists. Using existing source."
            ))
        
        try:
            self.stdout.write(f"Fetching data from {url}...")
            parsed_data = get_weather_data(url)
     
            created_count = 0
            updated_count = 0
            
            self.stdout.write(f"Processing {len(parsed_data)} data entries...")
            
            for item in parsed_data:
                # Skip header or non-data rows
                if not item.get('year') or not item.get('jan'):
                    continue
                    
                year = int(item.get('year'))  # Convert year to integer
                
                # Process each month's data
                for month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 
                              'jul', 'aug', 'sep', 'oct', 'nov', 'dec']:
                    if month in item and item[month] not in ['---', '']:
                        # Convert month name to month number
                        month_num = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 
                                    'may': 5, 'jun': 6, 'jul': 7, 'aug': 8, 
                                    'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}[month]
                        
                        try:
                            # Create or update the weather data
                            obj, created = WeatherData.objects.update_or_create(
                                year=year,
                                month=month_num,
                                source=data_source,  # Use the data_source object directly
                                defaults={'value': float(item[month])}
                            )
                            
                            if created:
                                created_count += 1
                            else:
                                updated_count += 1
                        except ValueError:
                            self.stdout.write(self.style.WARNING(
                                f"Skipping invalid value for {year}-{month_num}: {item[month]}"
                            ))
            
            self.stdout.write(self.style.SUCCESS(
                f"Successfully processed data. Added {created_count} new records, updated {updated_count} records."
            ))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))