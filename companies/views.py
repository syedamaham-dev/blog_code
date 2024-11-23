from django.http import HttpResponse
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from easy_reach.utils.auth_utils import clerk_authenticated
from .models import Company
from .serializers import CompanySerializer

# Set up the logger
logger = logging.getLogger('company.resources')

def test_logging(request):
    logger.debug('This is a debug message')
    logger.info('This is an info message')
    logger.warning('This is a warning message')
    logger.error('This is an error message')
    logger.critical('This is a critical message')

    return HttpResponse('Logging is working!')



@api_view(["GET"])
@clerk_authenticated  # Protect this view with Clerk authentication
def companies_view(request):

    # Fetch and serialize company data
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)
    return Response({"companies": serializer.data}, status=status.HTTP_200_OK)
