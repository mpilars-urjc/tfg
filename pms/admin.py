from django.contrib import admin
from .models import claseCuentas, claseHabitacion, claseApartamento, claseInquilinos, clasePagos, claseTarjetas, claseVariables, claseReserva

# Register your models here.

admin.site.register(claseHabitacion)
admin.site.register(claseApartamento)
admin.site.register(claseVariables)
admin.site.register(claseReserva)
admin.site.register(clasePagos)
admin.site.register(claseInquilinos)
admin.site.register(claseCuentas)
admin.site.register(claseTarjetas)