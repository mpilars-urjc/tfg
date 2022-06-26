from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^import_habitaciones$', views.import_habitaciones),
    url(r'^import_apartamentos$', views.import_apartamentos),
    url(r'^import_contactos$', views.import_contactos),
    url(r'^import_demandas$', views.import_demandas),
    url(r'^panel-de-reservas$', views.listReservas),
    url(r'^panel-de-reservas/reserva/(?P<reserva_id>\d+)/$', views.showReserva),
    url(r'^panel-de-reservas/reserva/(?P<reserva_id>\d+)/checkin$', views.checkinReserva),
    url(r'^panel-de-reservas/reserva/(?P<reserva_id>\d+)/pay$', views.payReserva),
    url(r'^panel-de-reservas/reserva/(?P<reserva_id>\d+)/complete$', views.completeReserva),
    url(r'^panel-de-checkin$', views.checkinPanel),
    url(r'^planning-de-ocupacion$', views.planningOcupacion),
    url(r'^herramientas/calculadora$', views.herramienta_calculadora),
]