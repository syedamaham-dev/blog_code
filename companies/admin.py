# company/admin.py
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .resources import CompanyResource  # Import the resource class
from .models import Company, Email

class EmailInline(admin.TabularInline):
    model = Email
    extra = 1

@admin.register(Company)
class CompanyAdmin(ImportExportModelAdmin):
    resource_class = CompanyResource  # Use the resource class
    inlines = [EmailInline]
