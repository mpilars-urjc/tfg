from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^gestion-de-inmuebles$', views.listInmuebles),
    url(r'^gestion-de-inmuebles/nuevo$', views.newInmueble),
    url(r'^gestion-de-inmuebles/eliminar$', views.deleteInmueble),
    url(r'^gestion-de-inmuebles/inmueble/(?P<apartamento_id>\w{0,50})/$', views.showInmueble),
    url(r'^gestion-de-inmuebles/inmueble/(?P<apartamento_id>\w{0,50})/nueva$', views.newRoom),
    url(r'^gestion-de-inmuebles/inmueble/(?P<apartamento_id>\w{0,50})/eliminar$', views.deleteRoom),
    url(r'^gestion-de-comerciales$', views.listComerciales),
    url(r'^gestion-de-comerciales/nuevo$', views.newComerciales),
    url(r'^gestion-de-comerciales/eliminar/(?P<comercial_id>\w{0,50})/', views.disableComerciales),
    url(r'^gestion-de-comerciales/activar/(?P<comercial_id>\w{0,50})/', views.enableComerciales),
    url(r'^gestion-de-comerciales/comercial/(?P<comercial_id>\w{0,50})/', views.showComerciales),
    url(r'^gestion-de-variables$', views.editVariables),
]