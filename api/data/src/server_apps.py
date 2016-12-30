import os

from django.core.wsgi import get_wsgi_application
from channels.asgi import get_channel_layer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

http = get_wsgi_application()
websocket = get_channel_layer()
