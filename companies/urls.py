# urls.py

from django.urls import path
from .views import test_logging,companies_view

urlpatterns = [
    path('test-logging/', test_logging, name='test-logging'),
    path('companies-list/', companies_view, name='companies'),
]
