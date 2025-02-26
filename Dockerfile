FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Comment out static files collection since it's not configured
# RUN python manage.py collectstatic --noinput

# Expose the port
EXPOSE 8000

# Command to run the application with Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]