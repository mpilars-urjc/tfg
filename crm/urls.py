from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^calendario$', views.calendarComercial),
    url(r'^gestion-demanda$', views.listDemanda),
    url(r'^gestion-demanda/registro$', views.newDemanda),
    url(r'^gestion-demanda/demanda/(?P<demanda_id>\d+)/$', views.showDemanda),
    url(r'^gestion-demanda/demanda/(?P<demanda_id>\d+)/edit$', views.editDemanda),
    url(r'^gestion-demanda/demanda/(?P<demanda_id>\d+)/visit$', views.visitDemanda),
    url(r'^gestion-demanda/demanda/(?P<demanda_id>\d+)/sale$', views.saleDemanda),
    url(r'^gestion-demanda/demanda/(?P<demanda_id>\d+)/lost$', views.lostDemanda),
    url(r'^gestion-demanda/demanda/(?P<demanda_id>\d+)/complete$', views.completeDemanda)
]