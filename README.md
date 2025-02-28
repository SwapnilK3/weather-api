# UK MetOffice Weather API

A Django REST API application to parse, store, and serve weather data from the UK MetOffice.

## Features

- Fetches and parses data from UK MetOffice data files
- Stores data in a structured database
- Provides a RESTful API to access the data
- Supports filtering by region, parameter, year, month, etc.
- Modern UI for data visualization and interaction
- Interactive data visualizations with multiple chart types
- Support for comparing regions, parameters, and time periods
- Pagination with 100 records per page

## Project Structure

The project is organized into several directories and files:

weather-api/
├── api/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── management/
│   │   ├── __init__.py
│   │   └── commands/
│   │       ├── __init__.py
│   │       └── fetch_weather_data.py
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── core/
│   ├── __init__.py
│   ├── asgi.py
│   ├── exceptions.py
│   ├── settings.py
│   ├── settings_prod.py
│   ├── urls.py
│   └── wsgi.py
├── utils/
│   ├── __init__.py
│   ├── data_fetcher.py
│   └── parsers.py
├── .gitignore
├── Dockerfile
├── README.md
├── docker-compose.yml
├── manage.py
└── requirements.txt

- **api/**: Contains the main application logic, including models, views, serializers, and URL routing.
- **api/templates/**: Contains HTML templates for the web interface.
- **api/tests/**: Contains test files for various components of the application.
- **core/**: Contains the core Django project settings and entry points for ASGI and WSGI.
- **api/management/**: Contains custom Django management commands for fetching and parsing weather data.
- **utils/**: Contains utility functions for data parsing.
- **manage.py**: Command-line utility for interacting with the Django project.
- **requirements.txt**: Lists the dependencies required for the project.
- **Dockerfile**: Instructions for building a Docker image for the application.
- **docker-compose.yml**: Defines services for running the application in Docker.
- **pytest.ini**: Configuration for pytest testing.

## Setup
### Requirements

- Python 3.8+ (tested with 3.11.9)
- Django 4+ (tested with 5.1.6)
- Django REST Framework
- Docker & Docker Compose (for containerized deployment)

### Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Make Migrations : `python manage.py makemigrations`
   If above not works use `python manage.py makemigrations api`
6. Run migrations: `python manage.py migrate`

### Running the Development Server

```
python manage.py runserver
```

### Fetching Weather Data

## API Endpoints

### Weather Data Endpoints

- **GET /api/weather/**: List all weather data records (paginated, 100 records per page)
- **GET /api/weather/fetch_data/**: Trigger data fetching from UK MetOffice

### Filtering Options

- **GET /api/weather/?region=UK**: Filter weather data by region
- **GET /api/weather/?parameter=Tmax**: Filter by parameter type (Tmax, Tmin, Rainfall, etc.)
- **GET /api/weather/?year=2020**: Filter by specific year
- **GET /api/weather/?month=6**: Filter by specific month (1-12)
- **GET /api/weather/?year=2020&month=6**: Combine multiple filters
- **GET /api/weather/?page=2**: Pagination (100 records per page)

### Data Source Endpoints

The following endpoints are available for managing data sources:

- **GET /api/source/**: List all data sources
- **POST /api/source/add_source/**: Add a new data source and fetch its data
- **GET /api/source/get_regions/**: Get list of available regions

### API Documentation

- **GET /api/docs/**: Comprehensive API documentation with examples

## Web Interface

The application includes a modern, responsive web interface for interacting with the data:

- **Dashboard** (/api/): Overview with statistics and recent data
- **Weather Data** (/api/weather/): View and filter weather data with pagination
- **Weather Visualization** (/api/weather/visualize/): Interactive charts and visualizations
- **Data Sources** (/api/source/): Manage and view data sources
- **Add Data Source** (/api/source/add_source/): Form to add new data sources
- **Regions** (/api/source/get_regions/): View available regions
- **API Documentation** (/api/docs/): Interactive API documentation

## Visualization Features

The application includes comprehensive data visualization capabilities:

### Chart Types

- **Time Series**: View monthly data trends across multiple years
- **Regional Comparison**: Compare weather data across different UK regions
- **Parameter Comparison**: Compare different parameters (temperature, rainfall, etc.) for a region
- **Seasonal Analysis**: Analyze seasonal patterns with radar charts
- **Annual Trends**: Observe long-term trends with moving averages and trend lines
- **Regional Heatmap**: Visualize geographic distributions with color-coded heatmaps

### Filtering Options

The visualization interface supports multiple filtering options:

- **Region**: Select specific UK regions or view all regions
- **Parameter**: Choose from available weather parameters (Tmax, Tmin, Rainfall, etc.)
- **Year**: Select a specific year for detailed analysis
- **Year Range**: Specify start and end years for long-term analysis

### Visualization Features

- Interactive charts with tooltips and legends
- Responsive design for desktop and mobile devices
- Parameter-specific color schemes (blue-red for temperature, blue for rainfall, etc.)
- Statistical summaries and extreme value detection
- Trend analysis with moving averages and regression lines
- Seasonal pattern detection and comparison
- Automatic unit selection based on parameter type (°C, mm, hours, etc.)

## Running with Docker

### Prerequisites
- Docker installed on your machine
- Docker Compose installed (included with Docker Desktop for Windows/Mac)

### Build and Run

1. **Using Docker Compose** (recommended):
```
docker-compose up
```

Or in detached mode:
```
docker-compose up -d
```

## Accessing the API

Once running, the API will be available at:
- Web interface: http://127.0.0.1:8000/api/
- API endpoints: http://127.0.0.1:8000/api/weather/, http://127.0.0.1:8000/api/source/, etc.

## Testing

The project includes comprehensive tests using pytest and Django's testing framework:

```bash
# Run all tests
python -m pytest

# Run with verbose output
python -m pytest -v

# Run specific test files
python -m pytest api/tests/test_models.py
python -m pytest api/tests/test_api.py

# Run with coverage report
pytest --cov=api
```
## Testing with Docker
 ```
 docker-compose run web pytest
 ```

 ## Deployment
 this will be updated tomorrow


##
This project is licensed under the MIT License. See the LICENSE file for more details.## LicenseThis application can be deployed on any cloud server that supports Docker. Ensure that the environment variables and database configurations are set correctly in the production environment.## Deployment```python manage.py test``` 
<!-- To run the tests, use the following command:## Testing   ```
API documentation is available at:

- Swagger UI: `/swagger/` -->


This project is licensed under the MIT License. See the LICENSE file for more details.


This updated README now includes:

1. Information about the web UI and available pages
2. Complete testing instructions with pytest
3. Docker deployment instructions
4. Updated project structure with templates and tests folders
5. Pagination information (100 records per page)
6. Cleaner formatting and organization

The README now accurately reflects the current state of your project including the UI components, Docker setup, and testing infrastructure.
This updated README now includes:

1. Information about the web UI and available pages
2. Complete testing instructions with pytest
3. Docker deployment instructions
4. Updated project structure with templates and tests folders
5. Pagination information (100 records per page)
6. Cleaner formatting and organization

The README now accurately reflects the current state of your project including the UI components, Docker setup, and testing infrastructure.

## Demo Video

<video controls src="https://github.com/SwapnilK3/weather-api/blob/main/demo.mp4" title="https://github.com/SwapnilK3/weather-api/blob/main/demo.mp4"></video>

[View Demo Video](https://github.com/SwapnilK3/weather-api/blob/main/demo.mp4)

