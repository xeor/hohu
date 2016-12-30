from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^_/api/admin/', admin.site.urls),
    url(r'^_/api/infoscreen/', include('apps.infoscreen.urls', namespace='inforscreen')),
]

from django.conf import settings
if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(url(r'^_/api/__debug__/', include(debug_toolbar.urls)))
