from django.contrib import admin
from .models import claseComercial, claseContacto, claseDemanda

# Register your models here.

admin.site.register(claseComercial)
admin.site.register(claseContacto)
admin.site.register(claseDemanda)