import os
import django
import pytest

# Set up Django before tests run
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()