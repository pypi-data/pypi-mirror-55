from django.conf.urls import url, include

urlpatterns = [
    url(r'^oauth2/', include('django_auth_adfs.urls')),
    url(r'^oauth2/', include('django_auth_adfs.drf_urls')),
]
