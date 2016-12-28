from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^infoscreen/', include('apps.infoscreen.urls', namespace='inforscreen')),
]
