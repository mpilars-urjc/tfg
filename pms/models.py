from django.db import models

# Create your models here.

class claseHabitacion(models.Model):

    """
    Una clase para definir los datos básicos de un comercial.
    """

    # Campos
    habitacionIdentificador = models.CharField(max_length=12)
    habitacionMetros = models.DecimalField(max_digits=4, decimal_places=2)
    habitacionBanos = models.IntegerField()
    habitacionAseos = models.IntegerField()
    habitacionVentanas = models.BooleanField()
    habitacionAscensor = models.BooleanField()
    habitacionBalcon = models.BooleanField()
    LOAN_CAMAS = (
        ('1', '90x190'),
        ('2', '105x190'),
        ('3', '135x190'),
        ('4', '150x190'),
        ('5', '2 (90x190)')
    )
    habitacionCama = models.CharField(max_length=1, choices=LOAN_CAMAS, default='1')
    LOAN_TIPO = (
        ('INT', 'Interior'),
        ('EXT', 'Exterior'),
    )
    habitacionTipo = models.CharField(max_length=3, choices=LOAN_TIPO, default='INT')
    LOAN_USO = (
        ('IND', 'Individual'),
        ('DOB', 'Doble'),
    )
    habitacionUso = models.CharField(max_length=3, choices=LOAN_USO, default='IND')
    habitacionFechaDeAlta = models.DateTimeField(auto_now_add=True)
    habitacionOcupacion = models.TextField()
    ...

    # Metadata
    class Meta:
        ordering = ["habitacionIdentificador"]

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
        return '%s | Metros: %s Baños: %s+%s Ventana: %s Ascensor: %s Balcón: %s Cama: %s Tipo: %s Uso: %s' % (self.habitacionIdentificador, self.habitacionMetros, self.habitacionBanos, self.habitacionAseos, self.habitacionVentanas, self.habitacionAscensor, self.habitacionBalcon, self.habitacionCama, self.habitacionTipo, self.habitacionUso)

class claseApartamento(models.Model):

    # Campos
    apartamentoIdentificador = models.CharField(max_length=5)
    apartamentoPais = models.CharField(max_length=20)
    apartamentoEstado = models.CharField(max_length=20)
    apartamentoCiudad = models.CharField(max_length=20)
    apartamentoCalle = models.CharField(max_length=40)
    apartamentoNumero = models.CharField(max_length=20)
    apartamentoPiso = models.CharField(max_length=20)
    apartamentoLetra = models.CharField(max_length=20)
    apartamentoCP = models.CharField(max_length=5)
    apartamentoOtros = models.CharField(max_length=20)
    apartamentoFechaDeAlta = models.DateTimeField(auto_now_add=True)
    ...

    # Metadata
    class Meta:
        ordering = ["apartamentoIdentificador"]

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
        return '%s | %s %s %s %s, %s %s %s (%s)' % (self.apartamentoIdentificador, self.apartamentoCalle, self.apartamentoNumero, self.apartamentoPiso, self.apartamentoLetra, self.apartamentoCiudad, self.apartamentoEstado, self.apartamentoPais, self.apartamentoCP)

class claseVariables(models.Model):

    # Campos
    varCalculadoraTipoInt = models.DecimalField(max_digits=4, decimal_places=2)
    varCalculadoraTipoExt = models.DecimalField(max_digits=4, decimal_places=2)
    varCalculadoraUsoInd = models.DecimalField(max_digits=4, decimal_places=2)
    varCalculadoraUsoDob = models.DecimalField(max_digits=4, decimal_places=2)
    varCalculadoraHab4 = models.DecimalField(max_digits=4, decimal_places=2)
    varCalculadoraHab5 = models.DecimalField(max_digits=4, decimal_places=2)
    varCalculadoraHab6 = models.DecimalField(max_digits=4, decimal_places=2)
    varCalculadoraHab7 = models.DecimalField(max_digits=4, decimal_places=2)
    varCalculadoraHab8 = models.DecimalField(max_digits=4, decimal_places=2)
    varCalculadoraHabPlus = models.DecimalField(max_digits=4, decimal_places=2)
    varCalculadoraBalSi = models.DecimalField(max_digits=4, decimal_places=2)
    varCalculadoraBalNo = models.DecimalField(max_digits=4, decimal_places=2)
    varCalculadoraAscSi = models.DecimalField(max_digits=4, decimal_places=2)
    varCalculadoraAscNo = models.DecimalField(max_digits=4, decimal_places=2)
    varCalculadoraCama90 = models.DecimalField(max_digits=4, decimal_places=2)
    varCalculadoraCama105 = models.DecimalField(max_digits=4, decimal_places=2)
    varCalculadoraCama135 = models.DecimalField(max_digits=4, decimal_places=2)
    varCalculadoraCama150 = models.DecimalField(max_digits=4, decimal_places=2)
    varCalculadoraCama2x90 = models.DecimalField(max_digits=4, decimal_places=2)
    varCalculadoraZona1 = models.DecimalField(max_digits=4, decimal_places=2)
    varCalculadoraZona2 = models.DecimalField(max_digits=4, decimal_places=2)
    varCalculadoraZona3 = models.DecimalField(max_digits=4, decimal_places=2)

    # Metadata
    class Meta:
        ordering = []

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
        return '%s' % (self.id)

class claseReserva(models.Model):
    """
    Una clase para definir los datos básicos de un contacto o persona interesada en un alquiler.
    """

    # Campos
    reservaId = models.AutoField(primary_key=True)
    demandaId = models.IntegerField()
    reservaContacto = models.CharField(max_length=10)
    reservaComercial = models.CharField(max_length=10)
    reservaApartamento = models.CharField(max_length=5)
    reservaHabitacion = models.CharField(max_length=12)
    reservaFRegistro = models.DateTimeField(auto_now_add=False)
    reservaFEntrada = models.DateTimeField(auto_now_add=False, null=True)
    reservaFSalida = models.DateTimeField(auto_now_add=False, null=True)
    reservaFPago = models.DateTimeField(auto_now_add=False, null=True)
    LOAN_PAGO = (
        ('1', 'Efectivo'),
        ('2', 'Tarjeta'),
        ('3', 'Transferencia'),
        ('4', 'Domicialiación')
    )
    reservaFormaPago = models.CharField(max_length=3, choices=LOAN_PAGO, default='1')
    LOAN_TIPO = (
        ('1', 'Único'),
        ('2', 'Mensual'),
        ('3', 'Trimestral'),
        ('4', 'Anual')
    )
    reservaTipoPago = models.CharField(max_length=3, choices=LOAN_TIPO, default='1')
    reservaPago = models.IntegerField(default=0)
    reservaObservaciones = models.CharField(max_length=200)
    reservaHistAcciones = models.CharField(max_length=10000)
    reservaIniciada = models.BooleanField(default=False)
    reservaCompletada = models.BooleanField(default=False)

    # Metadata
    class Meta:
        ordering = ["reservaFRegistro"]

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
        return '%s %s | %s %s %s %s | %s %s | Iniciada: %s Completada: %s' % (self.reservaId, self.demandaId, self.reservaContacto, self.reservaComercial, self.reservaApartamento, self.reservaHabitacion, self.reservaFEntrada, self.reservaFSalida, self.reservaIniciada, self.reservaCompletada)

class clasePagos(models.Model):
    """
    Una clase para definir los datos básicos de un contacto o persona interesada en un alquiler.
    """

    # Campos
    pagoId = models.AutoField(primary_key=True)
    reservaId = models.IntegerField()
    pagoFecha = models.DateTimeField(auto_now_add=False)
    pagoImporte = models.IntegerField(default=0)
    LOAN_PAGO = (
        ('1', 'Efectivo'),
        ('2', 'Tarjeta'),
        ('3', 'Transferencia'),
    )
    pagoForma = models.CharField(max_length=3, choices=LOAN_PAGO, default='1')
    pagoCompletado = models.BooleanField(default=False)
    pagoPlazoTotal = models.IntegerField()
    pagoPlazoActual = models.IntegerField()

    # Metadata
    class Meta:
        ordering = ["pagoId"]

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
        return '%s | %s | %s %s %s | %s/%s | %s' % (self.pagoId, self.reservaId, self.pagoFecha, self.pagoImporte, self.pagoForma, self.pagoPlazoActual, self.pagoPlazoTotal, self.pagoCompletado)

class claseTarjetas(models.Model):
    """
    Una clase para definir los datos básicos de un contacto o persona interesada en un alquiler.
    """

    # Campos
    tarjetaId = models.AutoField(primary_key=True)
    reservaId = models.IntegerField()
    tarjetaNum = models.IntegerField()
    tarjetaAno = models.IntegerField()
    tarjetaMes = models.IntegerField()
    tarjetaCVV = models.IntegerField()
    tarjetaTitular = models.CharField(max_length=50)

    # Metadata
    class Meta:
        ordering = ["tarjetaId"]

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
        return '%s | %s | %s | %s %s/%s (%s)' % (self.tarjetaId, self.reservaId, self.tarjetaTitular, self.tarjetaNum, self.tarjetaMes, self.tarjetaAno, self.tarjetaCVV)

class claseCuentas(models.Model):
    """
    Una clase para definir los datos básicos de un contacto o persona interesada en un alquiler.
    """

    # Campos
    cuentaId = models.AutoField(primary_key=True)
    reservaId = models.IntegerField()
    cuentaNum = models.CharField(max_length=24)
    cuentaTitular = models.CharField(max_length=50)

    # Metadata
    class Meta:
        ordering = ["cuentaId"]

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
        return '%s | %s | %s | %s' % (self.cuentaId, self.reservaId, self.cuentaTitular, self.cuentaNum)

class claseInquilinos(models.Model):
    """
    Una clase para definir los datos básicos de un contacto o persona interesada en un alquiler.
    """

    # Campos
    inquilinoId = models.AutoField(primary_key=True)
    reservaId = models.IntegerField()
    inquilinoNombre = models.CharField(max_length=100)
    inquilinoApellidos = models.CharField(max_length=100)
    inquilinoDni = models.CharField(max_length=100, default="")
    inquilinoTitular = models.BooleanField(default=False)

    # Metadata
    class Meta:
        ordering = ["inquilinoId"]

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
        return '%s | %s | %s %s %s' % (self.inquilinoId, self.reservaId, self.inquilinoDni, self.inquilinoNombre, self.inquilinoApellidos)