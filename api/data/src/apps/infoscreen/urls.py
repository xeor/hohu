from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Infoscreen.as_view(), name='_index'),
    url(r'^view/$', views.ViewList.as_view(), name='view-list'),
    url(r'^view/(?P<name>[a-zA-Z0-9\.-]+)', views.ViewDetail.as_view(), name='view-detail')
]
