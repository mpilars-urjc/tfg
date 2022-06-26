from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import include
from tfgsite.views import index


urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('pms/', include('pms.urls')),
    path('crm/', include('crm.urls')),
    path('channelmanager/', include('channelmanager.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
