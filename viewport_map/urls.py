from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from .map.api import LocationPointList
from .map.views import MapView

urlpatterns = [
    url(r'^$', MapView.as_view(), name='map_view'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/locations/$', LocationPointList.as_view(), name='list_points'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_URL
    )
