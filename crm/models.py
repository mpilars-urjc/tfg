from django.db import models

class claseComercial(models.Model):
    """
    Una clase para definir los datos básicos de un comercial.
    """

    # Campos
    comercialNombre = models.CharField(max_length=20)
    comercialApellido = models.CharField(max_length=40)
    comercialDNI = models.CharField(max_length=10)
    comercialFechaDeAlta = models.DateTimeField(auto_now_add=True)
    comercialActivo = models.BooleanField(default=True)
    ...

    # Metadata
    class Meta:
        ordering = ["comercialApellido", "-comercialFechaDeAlta"]

    # Métodos
    def get_absolute_url(self):
         """
         Devuelve la url para acceder a una instancia particular de MyModelName.
         """
         return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """
        Cadena para representar el objeto claseComercial (en el sitio de Admin, etc.)
        """
        return '%s %s | %s | %s' % (self.comercialNombre, self.comercialApellido, self.comercialDNI, self.comercialFechaDeAlta)

class claseContacto(models.Model):
    """
    Una clase para definir los datos básicos de un contacto o persona interesada en un alquiler.
    """

    # Campos
    contactoNombre = models.CharField(max_length=20)
    contactoApellido = models.CharField(max_length=40)
    contactoEmail = models.CharField(max_length=50)
    contactoTelefono = models.CharField(max_length=9)
    contactoDNI = models.CharField(max_length=10)
    contactoFechaDeAlta = models.DateTimeField(auto_now_add=True)
    ...

    # Metadata
    class Meta:
        ordering = ["contactoApellido", "-contactoFechaDeAlta"]

    # Métodos
    def get_absolute_url(self):
         """
         Devuelve la url para acceder a una instancia particular de MyModelName.
         """
         return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """
        Cadena para representar el objeto claseComercial (en el sitio de Admin, etc.)
        """
        return '%s %s | %s | %s | %s | %s' % (self.contactoNombre, self.contactoApellido, self.contactoDNI, self.contactoTelefono, self.contactoEmail, self.contactoFechaDeAlta)

class claseDemanda(models.Model):
    """
    Una clase para definir los datos básicos de un contacto o persona interesada en un alquiler.
    """

    # Campos
    demandaId = models.AutoField(primary_key=True)
    demandaContacto = models.CharField(max_length=10)
    demandaComercial = models.CharField(max_length=10)
    demandaApartamento = models.CharField(max_length=5)
    demandaHabitacion = models.CharField(max_length=12)
    demandaFRegistro = models.DateTimeField(auto_now_add=False)
    demandaFAsignacion = models.DateTimeField(auto_now_add=False, null=True)
    demandaFVisita = models.DateTimeField(auto_now_add=False, null=True)
    demandaVisObservaciones = models.CharField(max_length=200)
    demandaFOferta = models.DateTimeField(auto_now_add=False, null=True)
    demandaOferta  = models.IntegerField(default=0)
    demandaFCierre = models.DateTimeField(auto_now_add=False, null=True)
    demandaFEntrada = models.DateTimeField(auto_now_add=False, null=True)
    demandaFSalida = models.DateTimeField(auto_now_add=False, null=True)
    demandaObservaciones = models.CharField(max_length=200)
    demandaHistAcciones = models.CharField(max_length=10000)
    demandaPerdida =models.BooleanField(default=False)
    demandaGanada = models.BooleanField(default=False)

    # Metadata
    class Meta:
        ordering = ["demandaFRegistro"]

    # Métodos
    def get_absolute_url(self):
         """
         Devuelve la url para acceder a una instancia particular de MyModelName.
         """
         return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """
        Cadena para representar el objeto claseComercial (en el sitio de Admin, etc.)
        """
        return '%s | %s %s %s | %s | %s | %s | %s | %s | %s' % (self.demandaId, self.demandaContacto, self.demandaComercial, self.demandaApartamento, self.demandaFRegistro, self.demandaFAsignacion, self.demandaFVisita, self.demandaFOferta, self.demandaFCierre, self.demandaObservaciones)