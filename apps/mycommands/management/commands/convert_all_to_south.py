import settings
from django.core.management.base import BaseCommand
from subprocess import call

class Command(BaseCommand):
    
    def _is_project_app(self, app_name):
        return not 'django' in app_name and not 'south' in app_name
    
    def handle(self, *args, **options):
        try:
            call(['./manage.py', 'syncdb'])
            
            for app in settings.INSTALLED_APPS:
                if self._is_project_app(app):
                    call(['./manage.py', 'convert_to_south', app])
                    
            print 'All applications converted to south'
        except:
            pass

