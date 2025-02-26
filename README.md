# UK MetOffice Weather API

A Django REST API application to parse, store, and serve weather data from the UK MetOffice.

## Features

- Fetches and parses data from UK MetOffice data files
- Stores data in a structured database
- Provides a RESTful API to access the data
- Supports filtering by region, parameter, year, month, etc.

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
- **core/**: Contains the core Django project settings and entry points for ASGI and WSGI.
- **api/management/**: Contains custom Django management commands for fetching and parsing weather data.
- **utils/**: Contains utility functions for data parsing.
- **manage.py**: Command-line utility for interacting with the Django project.
- **requirements.txt**: Lists the dependencies required for the project.
- **Dockerfile**: Instructions for building a Docker image for the application.
- **docker-compose.yml**: Defines services for running the application in Docker.


## Setup
### Requirements

- Python 3.8+ (mine is 3.11.9)
- Django 4+ (mine is 5.1.6)
- Django REST Framework

### Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Make Migrations : `python manage.py makemigrations`
if above not works use `python manage.py makemigrations api`

6. Run migrations: `python manage.py migrate`


### Running the Development Server

```
python manage.py runserver
```

### Fetching Weather Data

## API Endpoints

### Weather Data Endpoints

- **GET /api/weather/**: List all weather data records (paginated)
- **GET /api/weather/get_data/**: Retrieve a specific weather data record
- **POST /api/weather/fetch_data/**: Trigger data fetching from UK MetOffice

### Filtering Options

- **GET /api/weather/?region=UK**: Filter weather data by region
- **GET /api/weather/?parameter=Tmax**: Filter by parameter type (Tmax, Tmin, Rainfall, etc.)
- **GET /api/weather/?year=2020**: Filter by specific year
- **GET /api/weather/?month=6**: Filter by specific month (1-12)
- **GET /api/weather/?year=2020&month=6**: Combine multiple filters


### Data Source Endpoints

The following endpoints are available for managing data sources:

- **GET /api/source/**: List all data sources (read-only)
- **POST /api/source/add_source/**: Add a new data source
- **GET /api/source/get_regions/**: Get list of available regions
- **GET /api/sources/**: List all available data sources


<!-- ### API Documentation

- **GET /swagger/**: Interactive Swagger UI documentation
- **GET /redoc/**: Alternative ReDoc documentation
- **GET /swagger.json**: OpenAPI specification in JSON format -->

## Running with Docker

### Prerequisites
- Docker installed on your machine
- Docker Compose installed (included with Docker Desktop for Windows/Mac)

### Build and Run

1. **Build the Docker image**:
```
docker build -t weather-api .
```



2. **Run the application using Docker Compose**:
  ``` 
  docker run -p 8000:8000 weather-api
  ```


3. **Using Docker Compose**:

Create a `docker-compose.yml` file with the following contents:
```yaml
version: '3'

services:
  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_DB=weather_db
      - POSTGRES_USER=weather_user
      - POSTGRES_PASSWORD=weather_password
    ports:
      - "5432:5432"

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      - DEBUG=1
      - DJANGO_SECRET_KEY=dev_key_change_in_production
    depends_on:
      - db

volumes:
  postgres_data:

```
Then run:

```
docker-compose up
```

Or in detached mode:
```
docker-compose up -d
```

## Accessing the API
Once running in Docker, the API will be available at http://127.0.0.1:8000/api/

## Testing
this also will be updated tomorrow
<!-- To run the tests, use the following command::
```
python manage.py test image**:python manage.py test
``````
   docker build -t weather-api . -->
 ## Deployment
 this will be updated tomorrow
<!--
2. **Run the application using Docker Compose**:cation can be deployed on any cloud server that supports Docker. Ensure that the environment variables and database configurations are set correctly in the production environment.
   ```
   docker-compose up
   ``` -->

##
This project is licensed under the MIT License. See the LICENSE file for more details.## LicenseThis application can be deployed on any cloud server that supports Docker. Ensure that the environment variables and database configurations are set correctly in the production environment.## Deployment```python manage.py test``` 
<!-- To run the tests, use the following command:## Testing   ```
API documentation is available at:

- Swagger UI: `/swagger/` -->


This project is licensed under the MIT License. See the LICENSE file for more details.
<!-- - ReDoc: `/redoc/` -->

<!-- ## License -->