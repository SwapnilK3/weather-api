from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.db import IntegrityError
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    Custom exception handler for better error messages
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    # Log the error
    logger.error(f"Exception: {str(exc)} in {context['view'].__class__.__name__}")
    
    # If response is not defined, create a custom one
    if response is None:
        if isinstance(exc, IntegrityError):
            response = Response({
                'error': 'Database integrity error',
                'detail': str(exc)
            }, status=400)
        elif isinstance(exc, ValueError):
            response = Response({
                'error': 'Value error',
                'detail': str(exc)
            }, status=400)
        else:
            response = Response({
                'error': 'Internal server error',
                'detail': str(exc)
            }, status=500)
    
    return response