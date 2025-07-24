
# wsgi.py 
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tiktopApi.settings')
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")


application = get_wsgi_application()


# config/
# ├── __init__.py            ✅ recommended!
# ├── settings/
# │   ├── __init__.py        ✅ required!
# │   ├── base.py
# │   ├── dev.py
# │   └── prod.py
# ├── urls.py
# ├── asgi.py
# └── wsgi.py
