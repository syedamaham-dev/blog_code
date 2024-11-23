from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Company, Email

class CompanyResource(resources.ModelResource):
    email = fields.Field(attribute='email', column_name='email')

    class Meta:
        model = Company
        fields = ('name', 'email', 'url', 'is_active', 'country', 'city')
        import_id_fields = ('name', 'url')
    
    def before_import_row(self, row, **kwargs):
        name = row.get('name')
        url = row.get('url')
        email_list = row.get('email')

        # Handle missing email case
        if not email_list or email_list.strip() == '':
            print(f"Skipping row: Missing email for company '{name}' with URL '{url}'")
            return None  # Skip this row if email is missing
        
        # Handle multiple emails (separated by commas) or single email
        emails = [email.strip() for email in email_list.split(',')] if ',' in email_list else [email_list.strip()]
        # Check if the company already exists (based on 'name' and 'url')
        existing_company = Company.objects.filter(name=name, url=url).exists()
        if existing_company:
            print(f"Skipping row: Company with name '{name}' and URL '{url}' already exists")
            return None  # Skip this row if company already exists
        # Store
        row['email'] = emails
        return row
    
    def after_save_instance(self, instance, row, **kwargs):
        emails = row.get('email')
        if emails:
            for email in emails:
                Email.objects.create(email=email, company=instance)
                
        return instance
    