from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from crm.models import claseComercial, claseContacto, claseDemanda
from pms.models import claseApartamento, claseHabitacion, claseReserva
from custom.disponibilidad import check
from custom.pagos import generarPagos

from datetime import datetime, timedelta


# Create your views here.
@login_required
def  listDemanda(request):
    if request.user.groups.filter(name="CRM").exists():
        if request.method == "GET":
            listadoDemanda = claseDemanda.objects.order_by("demandaFEntrada").filter(demandaPerdida=False).filter(demandaGanada=False)
            status = []

            total = 0
            for item in listadoDemanda:
                total = total + 1
                contactoId = item.demandaContacto
                tempContacto = claseContacto.objects.get(contactoDNI=contactoId)
                item.demandaContacto = tempContacto.contactoNombre + " " + tempContacto.contactoApellido

                comercialId = item.demandaComercial
                if comercialId == 'none':
                    item.demandaComercial = 'No asignado'
                else:
                    tempComercial = claseComercial.objects.get(comercialDNI=comercialId)
                    item.demandaComercial = tempComercial.comercialNombre + " " + tempComercial.comercialApellido

                apartamentoId = item.demandaApartamento
                tempApartamento = claseApartamento.objects.get(apartamentoIdentificador=apartamentoId)
                item.demandaApartamento = tempApartamento.apartamentoIdentificador + " | " + tempApartamento.apartamentoCalle + " " + tempApartamento.apartamentoNumero + " " + tempApartamento.apartamentoPiso + tempApartamento.apartamentoLetra + " (" + tempApartamento.apartamentoCiudad + ")"

                fechaEntrada = item.demandaFEntrada
                item.demandaFEntrada = fechaEntrada.strftime("%d/%m/%Y")
                fechaSalida = item.demandaFSalida
                item.demandaFSalida = fechaSalida.strftime("%d/%m/%Y")
                status.append(check(fechaEntrada, fechaSalida, item.demandaHabitacion, item.demandaId))
                fechaRegistro = item.demandaFRegistro
                item.demandaFRegistro = fechaRegistro.strftime("%d/%m/%Y")
            
            return render(request,"crm/listDemanda.html",
            context={"demandas": listadoDemanda,
                        "estados":status,
                        "totDemandas": total})
    else:
        return render(request,"noaccess.html")

@login_required
def  newDemanda(request):
    if request.user.groups.filter(name="CRM").exists():
        if request.method == "GET":
            ## Iniciando variables
            now = datetime.now()

            # Preparar lista de comerciales para botón de selección
            listadoComercial = claseComercial.objects.order_by("comercialNombre").filter(comercialActivo=True)

            # Preparar lista de apartamentos para botón de selección
            listadoApartamento = claseApartamento.objects.order_by("apartamentoIdentificador")

            # Preparar lista de apartamentos para botón de selección
            listadoHabitacion = claseHabitacion.objects.order_by("habitacionIdentificador")
            for item in listadoHabitacion:
                if item.habitacionCama == "1":
                    item.habitacionCama = "90x190"
                elif item.habitacionCama == "2":
                    item.habitacionCama = "105x190"
                elif item.habitacionCama == "3":
                    item.habitacionCama = "135x190"
                elif item.habitacionCama == "4":
                    item.habitacionCama = "150x190"
                elif item.habitacionCama == "5":
                    item.habitacionCama = "2(90x190)"

                if item.habitacionUso == "IND":
                    item.habitacionUso = "individual"
                elif item.habitacionUso == "DOB":
                    item.habitacionUso = "doble"

                if item.habitacionTipo == "INT":
                    item.habitacionTipo = "interior"
                elif item.habitacionTipo == "EXT":
                    item.habitacionTipo = "exterior"

            fechaHoy = now.strftime("%Y-%m-%d")

            return render(request,"crm/newDemanda.html",
                context={"listadoComercial":listadoComercial,
                        "listadoApartamento":listadoApartamento,
                        "listadoHabitacion":listadoHabitacion,
                        "fechaHoy":fechaHoy,
                        })

        elif request.method == "POST":
            now = datetime.now()
            listadoComercial = claseComercial.objects.order_by("comercialNombre")
            listadoApartamento = claseApartamento.objects.order_by("apartamentoIdentificador")

            dataPost = request.POST
            fechaEntrada = datetime.strptime(dataPost["fechaEntrada"], '%d/%m/%Y') + timedelta(hours=6)
            fechaSalida = datetime.strptime(dataPost["fechaSalida"], '%d/%m/%Y') + timedelta(hours=6)
            postNombreContacto = dataPost['contNombre'] + " " + dataPost["contApellidos"]
            postDniContacto = dataPost['contDni']
            postTelefonoContacto = dataPost['contTelefono']
            postEmailContacto = dataPost['contEmail']
            postDemObserv = dataPost['demObservaciones']
            if dataPost['idComercial'] == "none":
                postComercial = "Sin comercial asignado"
                date_comercial = None
            else:
                comercial = claseComercial.objects.get(comercialDNI=dataPost['idComercial'])
                postComercial = comercial.comercialNombre + " " + comercial.comercialApellido
                dateComercial = datetime.now()
            if dataPost['idApartamento'] == "none":
                postApartamento = "Sin apartamento asignado"
            else:
                apartamento = claseApartamento.objects.get(apartamentoIdentificador=dataPost['idApartamento'])
                postApartamento = apartamento.apartamentoIdentificador + " | " + apartamento.apartamentoCalle + " " + apartamento.apartamentoNumero + " " + apartamento.apartamentoPiso + apartamento.apartamentoLetra + " " + apartamento.apartamentoCiudad + " (" + apartamento.apartamentoEstado + ")"
                
            if claseContacto.objects.filter(contactoDNI=postDniContacto).exists():
                contacto = ""
            else:
                p = claseContacto.objects.create(
                    contactoNombre = dataPost["contNombre"],
                    contactoApellido = dataPost["contApellidos"],
                    contactoEmail = dataPost["contEmail"],
                    contactoTelefono = dataPost["contTelefono"],
                    contactoDNI = dataPost["contDni"]
                )
            
            demHistAccion = "[" + now.strftime("%d/%m/%Y %H:%M:%S") + "] [" + str(request.user) + "] Elemento creado correctamente"
            
            d = claseDemanda.objects.create(
                demandaContacto = postDniContacto,
                demandaComercial = dataPost["idComercial"],
                demandaApartamento = dataPost["idApartamento"],
                demandaHabitacion = dataPost["idHabitacion"],
                demandaFRegistro = now,
                demandaFAsignacion = dateComercial,
                demandaFVisita = None,
                demandaFOferta = None,
                demandaFCierre = None,
                demandaFEntrada = fechaEntrada,
                demandaFSalida = fechaSalida,
                demandaObservaciones = postDemObserv,
                demandaHistAcciones = demHistAccion
            )

            url = "/crm/gestion-demanda/demanda/" + str(d.demandaId)
            return redirect(url)
    else:
        return render(request,"noaccess.html")

@login_required
def  showDemanda(request, demanda_id):
    if request.user.groups.filter(name="CRM").exists():
        # Recogiendo información de todas las bases de datos
        tempDemanda = claseDemanda.objects.get(demandaId=demanda_id)
        tempContacto = claseContacto.objects.get(contactoDNI=tempDemanda.demandaContacto)
        tempComercial = claseComercial.objects.get(comercialDNI=tempDemanda.demandaComercial)
        tempApartamento = claseApartamento.objects.get(apartamentoIdentificador=tempDemanda.demandaApartamento)
        tempHabitacion = claseHabitacion.objects.get(habitacionIdentificador=tempDemanda.demandaHabitacion)

        # Datos del contacto
        contactoNombre = tempContacto.contactoNombre + " " + tempContacto.contactoApellido
        contactoDNI = tempContacto.contactoDNI
        contactoEmail = tempContacto.contactoEmail
        contactoTelefono = tempContacto.contactoTelefono

        # Datos del comercial
        comercialNombre = tempComercial.comercialNombre + " " + tempComercial.comercialApellido

        # Datos apartamento
        apartamentoId = tempApartamento.apartamentoIdentificador
        apartamentoDireccion = tempApartamento.apartamentoCalle + " " + tempApartamento.apartamentoNumero + " " + tempApartamento.apartamentoPiso + tempApartamento.apartamentoLetra + " (" + tempApartamento.apartamentoCiudad + ")"

        # Datos habitacion
        habitacionId = tempHabitacion.habitacionIdentificador
        habitacionTamano = tempHabitacion.habitacionMetros
        if tempHabitacion.habitacionAseos == 0:
            habitacionBanos = str(tempHabitacion.habitacionBanos) + " baños"
        else:
            habitacionBanos = str(tempHabitacion.habitacionBanos) + " baño(s) y " + str(tempHabitacion.habitacionAseos) + " aseo(s)"
        habitacionVentana = tempHabitacion.habitacionVentanas
        if habitacionVentana == True:
            habitacionVentana = "sí"
        else:
            habitacionVentana = "no"
        habitacionAscensor = tempHabitacion.habitacionAscensor
        if habitacionAscensor == True:
            habitacionAscensor = "sí"
        else:
            habitacionAscensor = "no"
        habitacionBalcon = tempHabitacion.habitacionBalcon
        if habitacionBalcon == True:
            habitacionBalcon = "sí"
        else:
            habitacionBalcon = "no"
        if tempHabitacion.habitacionCama == "1":
            habitacionCama = "90x190"
        elif tempHabitacion.habitacionCama == "2":
            habitacionCama = "105x190"
        elif tempHabitacion.habitacionCama == "3":
            habitacionCama = "135x190"
        elif tempHabitacion.habitacionCama == "4":
            habitacionCama = "150x190"
        elif tempHabitacion.habitacionCama == "5":
            habitacionCama = "2(90x190)"
        if tempHabitacion.habitacionUso == "IND":
            habitacionOcupacion = "individual"
        elif tempHabitacion.habitacionUso == "DOB":
            habitacionOcupacion = "doble"
        if tempHabitacion.habitacionTipo == "INT":
            habitacionTipologia = "interior"
        elif tempHabitacion.habitacionTipo == "EXT":
            habitacionTipologia = "exterior"

        # Fechas varias
        fechaRegistro = tempDemanda.demandaFRegistro.strftime("%d/%m/%Y")
        fechaEntrada = tempDemanda.demandaFEntrada.strftime("%d/%m/%Y")
        fechaSalida = tempDemanda.demandaFSalida.strftime("%d/%m/%Y")
        fechaAsignacion = tempDemanda.demandaFAsignacion.strftime("%d/%m/%Y")
        if tempDemanda.demandaFVisita != None:
            tempDemanda.demandaFVisita = tempDemanda.demandaFVisita + timedelta(hours=2)
            fechaVisita = tempDemanda.demandaFVisita.strftime("%d/%m/%Y %H:%M")
        else:
            fechaVisita = "no realizada"
        if tempDemanda.demandaFOferta != None:
            tempDemanda.demandaFOferta = tempDemanda.demandaFOferta + timedelta(hours=2)
            fechaOferta =tempDemanda.demandaFOferta.strftime("%d/%m/%Y")
        else:
            fechaOferta = "no realizada"
        if tempDemanda.demandaOferta != None and tempDemanda.demandaOferta != 0:
            oferta = str(tempDemanda.demandaOferta) + " EUR/MES"
        else:
            oferta = ""
        
        # Preparación de histórico
        historico = tempDemanda.demandaHistAcciones.split('||')

        # Comprobando disponibilidad
        status = check(tempDemanda.demandaFEntrada, tempDemanda.demandaFSalida, habitacionId, demanda_id)

        return render(request,"crm/showDemanda.html",
                context={"id":demanda_id,
                        "contactoNombre":contactoNombre,
                        "contactoDni":contactoDNI,
                        "contactoEmail":contactoEmail,
                        "contactoTelefono":contactoTelefono,
                        "comercialNombre":comercialNombre,
                        "apartamentoId":apartamentoId,
                        "apartamentoDireccion":apartamentoDireccion,
                        "habitacionId":habitacionId,
                        "habitacionTamano":habitacionTamano,
                        "habitacionBanos":habitacionBanos,
                        "habitacionVentana":habitacionVentana,
                        "habitacionAscensor":habitacionAscensor,
                        "habitacionBalcon":habitacionBalcon,
                        "habitacionCama":habitacionCama,
                        "habitacionOcupacion":habitacionOcupacion,
                        "habitacionTipologia":habitacionTipologia,
                        "fechaRegistro":fechaRegistro,
                        "fechaEntrada":fechaEntrada,
                        "fechaSalida":fechaSalida,
                        "fechaAsignacion":fechaAsignacion,
                        "fechaVisita":fechaVisita,
                        "fechaOferta":fechaOferta,
                        "oferta":oferta,
                        "historico":historico,
                        "status": status
                        })
    else:
        return render(request,"noaccess.html")

@login_required
def  editDemanda(request, demanda_id):
    if request.user.groups.filter(name="CRM").exists():
        if request.method == "GET":
            ## Iniciando variables
            now = datetime.now()
            tempDemanda = claseDemanda.objects.get(demandaId=demanda_id)
            tempContacto = claseContacto.objects.get(contactoDNI=tempDemanda.demandaContacto)
            tempComercial = claseComercial.objects.order_by("comercialNombre").filter(comercialActivo=True)
            tempApartamento = claseApartamento.objects.order_by("apartamentoIdentificador")
            tempHabitacion = claseHabitacion.objects.order_by("habitacionIdentificador")

            # Datos del contacto
            contactoNombre = tempContacto.contactoNombre 
            contactoApellido = tempContacto.contactoApellido
            contactoDNI = tempContacto.contactoDNI
            contactoEmail = tempContacto.contactoEmail
            contactoTelefono = tempContacto.contactoTelefono

            # Datos del comercial
            comercialDni = tempDemanda.demandaComercial

            # Datos apartamento
            apartamentoId = tempDemanda.demandaApartamento

            # Datos habitacion
            habitacionId = tempDemanda.demandaHabitacion    
            for item in tempHabitacion:
                if item.habitacionCama == "1":
                    item.habitacionCama = "90x190"
                elif item.habitacionCama == "2":
                    item.habitacionCama = "105x190"
                elif item.habitacionCama == "3":
                    item.habitacionCama = "135x190"
                elif item.habitacionCama == "4":
                    item.habitacionCama = "150x190"
                elif item.habitacionCama == "5":
                    item.habitacionCama = "2(90x190)"
                if item.habitacionUso == "IND":
                    item.habitacionUso = "individual"
                elif item.habitacionUso == "DOB":
                    item.habitacionUso = "doble"
                if item.habitacionTipo == "INT":
                    item.habitacionTipo = "interior"
                elif item.habitacionTipo == "EXT":
                    item.habitacionTipo = "exterior"
            
            # Fechas varias
            fechaEntrada = tempDemanda.demandaFEntrada.strftime("%d/%m/%Y")
            fechaSalida = tempDemanda.demandaFSalida.strftime("%d/%m/%Y")

            observaciones = tempDemanda.demandaObservaciones
            historico = tempDemanda.demandaHistAcciones.split('||')

            return render(request,"crm/editDemanda.html",
                context={"id":demanda_id,
                        "contactoDni":contactoDNI,
                        "contactoNombre":contactoNombre,
                        "contactoApellido":contactoApellido,
                        "contactoEmail":contactoEmail,
                        "contactoTelefono":contactoTelefono,
                        "comercialDni":comercialDni,
                        "apartamentoId":apartamentoId,
                        "habitacionId":habitacionId,
                        "fechaEntrada":fechaEntrada,
                        "fechaSalida":fechaSalida,
                        "observaciones":observaciones,
                        "historico":historico,
                        "listadoComercial":tempComercial,
                        "listadoApartamento":tempApartamento,
                        "listadoHabitacion":tempHabitacion
                        })

        elif request.method == "POST":
            now = datetime.now()
            dataPost = request.POST
            demandaOriginal = claseDemanda.objects.get(demandaId=demanda_id)

            modificacion = False

            # Datos originales
            originalComercialId = demandaOriginal.demandaComercial
            originalApartamentoId = demandaOriginal.demandaApartamento
            originalHabitacionId = demandaOriginal.demandaHabitacion
            originalObservaciones = demandaOriginal.demandaObservaciones
            originalFechaEntrada = demandaOriginal.demandaFEntrada.strftime("%d/%m/%Y")
            originalFechaSalida = demandaOriginal.demandaFSalida.strftime("%d/%m/%Y")
            originalDemandaHistAcciones = demandaOriginal.demandaHistAcciones

            # Datos recibidos del formulario
            contactoNombre = dataPost['contNombre']
            contactoApellidos = dataPost['contApellidos']
            contactoDni = dataPost['contDni']
            contactoTelefono = dataPost['contTelefono']
            contactoEmail = dataPost['contEmail']
            comercialId = dataPost['idComercial']
            apartamentoId = dataPost['idApartamento']
            habitacionId = dataPost['idHabitacion']
            observaciones = dataPost['demObservaciones']
            fechaEntrada = dataPost['fechaEntrada']
            fechaSalida = dataPost['fechaSalida']

            # Modificacion de comercial
            if originalComercialId != comercialId:
                modificacion = True

                originalComercial = claseComercial.objects.get(comercialDNI=originalComercialId)
                originalNombreComercial = originalComercial.comercialNombre + " " + originalComercial.comercialApellido
                nuevoComercial = claseComercial.objects.get(comercialDNI=comercialId)
                nuevoNombreComercial = nuevoComercial.comercialNombre + " " + nuevoComercial.comercialApellido

                demandaOriginal.demandaComercial = comercialId
                demandaOriginal.demandaHistAcciones = "[" + now.strftime("%d/%m/%Y %H:%M:%S") + "] [" + str(request.user) + "] Comercial asignado cambiado de " + originalNombreComercial + " a " + nuevoNombreComercial + ".||" + demandaOriginal.demandaHistAcciones

            # Modificacion de apartamento
            if originalApartamentoId != apartamentoId:
                modificacion = True

                demandaOriginal.demandaApartamento = apartamentoId
                demandaOriginal.demandaHabitacion = habitacionId
                demandaOriginal.demandaHistAcciones = "[" + now.strftime("%d/%m/%Y %H:%M:%S") + "] [" + str(request.user) + "] Apartamento cambiado de " + originalApartamentoId + " a " + apartamentoId + ".||" + demandaOriginal.demandaHistAcciones
                demandaOriginal.demandaHistAcciones = "[" + now.strftime("%d/%m/%Y %H:%M:%S") + "] [" + str(request.user) + "] Habitacion cambiada de " + originalHabitacionId + " a " + habitacionId + ".||" + demandaOriginal.demandaHistAcciones
                
            if originalApartamentoId == apartamentoId and originalHabitacionId != habitacionId:
                modificacion = True
                demandaOriginal.demandaHabitacion = habitacionId
                demandaOriginal.demandaHistAcciones = "[" + now.strftime("%d/%m/%Y %H:%M:%S") + "] [" + str(request.user) + "] Habitacion cambiada de " + originalHabitacionId + " a " + habitacionId + ".||" + demandaOriginal.demandaHistAcciones

            if originalFechaEntrada != fechaEntrada:
                modificacion = True
                demandaOriginal.demandaFEntrada = datetime.strptime(fechaEntrada, '%d/%m/%Y') + timedelta(hours=6)
                demandaOriginal.demandaHistAcciones = "[" + now.strftime("%d/%m/%Y %H:%M:%S") + "] [" + str(request.user) + "] Fecha de entrada cambiada de " + str(originalFechaEntrada) + " a " + str(fechaEntrada) + ".||" + demandaOriginal.demandaHistAcciones

            if originalFechaSalida != fechaSalida:
                modificacion = True
                demandaOriginal.demandaFSalida = datetime.strptime(fechaSalida, '%d/%m/%Y') + timedelta(hours=6)
                demandaOriginal.demandaHistAcciones = "[" + now.strftime("%d/%m/%Y %H:%M:%S") + "] [" + str(request.user) + "] Fecha de salida cambiada de " + str(originalFechaSalida) + " a " + str(fechaSalida) + ".||" + demandaOriginal.demandaHistAcciones

            if modificacion:
                demandaOriginal.save()

            url = "/crm/gestion-demanda/demanda/" + demanda_id + "/"
            return HttpResponseRedirect(url)
    else:
        return render(request,"noaccess.html")

@login_required
def  visitDemanda(request, demanda_id):
    if request.user.groups.filter(name="CRM").exists():
        if request.method == "GET":
            ## Iniciando variables
            now = datetime.now()
            tempDemanda = claseDemanda.objects.get(demandaId=demanda_id)
            tempContacto = claseContacto.objects.get(contactoDNI=tempDemanda.demandaContacto)

            # Datos del contacto
            contactoNombre = tempContacto.contactoNombre 
            contactoApellido = tempContacto.contactoApellido
            contactoDNI = tempContacto.contactoDNI
            contactoEmail = tempContacto.contactoEmail
            contactoTelefono = tempContacto.contactoTelefono

            # Fechas varias
            fechaRegistro = tempDemanda.demandaFRegistro.strftime("%d/%m/%Y")
            fechaEntrada = tempDemanda.demandaFEntrada.strftime("%d/%m/%Y")
            fechaSalida = tempDemanda.demandaFSalida.strftime("%d/%m/%Y")
            fechaAsignacion = tempDemanda.demandaFAsignacion.strftime("%d/%m/%Y")
            if tempDemanda.demandaFVisita != None:
                fechaVisita = tempDemanda.demandaFVisita.strftime("%d/%m/%Y")
            else:
                fechaVisita = "no realizada"
            if tempDemanda.demandaFOferta != None:
                fechaOferta =tempDemanda.demandaFOferta.strftime("%d/%m/%Y")
            else:
                fechaOferta = "no realizada"
            
            observaciones = tempDemanda.demandaObservaciones

            return render(request,"crm/visitDemanda.html",
                context={"id":demanda_id,
                        "contactoNombre":contactoNombre,
                        "contactoDni":contactoDNI,
                        "contactoEmail":contactoEmail,
                        "contactoTelefono":contactoTelefono,
                        "fechaRegistro":fechaRegistro,
                        "fechaEntrada":fechaEntrada,
                        "fechaSalida":fechaSalida,
                        "fechaAsignacion":fechaAsignacion,
                        "fechaVisita":fechaVisita,
                        "fechaOferta":fechaOferta
                        })

        elif request.method == "POST":
            now = datetime.now()
            dataPost = request.POST
            tempDemanda = claseDemanda.objects.get(demandaId=demanda_id)

            fechaVisita = dataPost["fechaVisita"]
            visitaObservaciones = dataPost["visObservaciones"]

            tempDemanda.demandaFVisita = datetime.strptime(fechaVisita, '%d/%m/%Y %H:%M')
            tempDemanda.demadaVisObservaciones = visitaObservaciones
            tempDemanda.demandaHistAcciones = "[" + now.strftime("%d/%m/%Y %H:%M:%S") + "] [" + str(request.user) + "] Añadida nueva fecha de visita: " + str(fechaVisita) + " (" + visitaObservaciones + ").||" + tempDemanda.demandaHistAcciones

            tempDemanda.save()

            url = "/crm/gestion-demanda/demanda/" + demanda_id + "/"
            return HttpResponseRedirect(url)
    else:
        return render(request,"noaccess.html")

@login_required
def  saleDemanda(request, demanda_id):
    if request.user.groups.filter(name="CRM").exists():
        if request.method == "GET":
            ## Iniciando variables
            now = datetime.now()
            tempDemanda = claseDemanda.objects.get(demandaId=demanda_id)
            tempContacto = claseContacto.objects.get(contactoDNI=tempDemanda.demandaContacto)

            # Datos del contacto
            contactoNombre = tempContacto.contactoNombre 
            contactoApellido = tempContacto.contactoApellido
            contactoDNI = tempContacto.contactoDNI
            contactoEmail = tempContacto.contactoEmail
            contactoTelefono = tempContacto.contactoTelefono

            # Fechas varias
            fechaRegistro = tempDemanda.demandaFRegistro.strftime("%d/%m/%Y")
            fechaEntrada = tempDemanda.demandaFEntrada.strftime("%d/%m/%Y")
            fechaSalida = tempDemanda.demandaFSalida.strftime("%d/%m/%Y")
            fechaAsignacion = tempDemanda.demandaFAsignacion.strftime("%d/%m/%Y")
            if tempDemanda.demandaFVisita != None:
                fechaVisita = tempDemanda.demandaFVisita.strftime("%d/%m/%Y")
            else:
                fechaVisita = "no realizada"
            if tempDemanda.demandaFOferta != None:
                fechaOferta =tempDemanda.demandaFOferta.strftime("%d/%m/%Y")
            else:
                fechaOferta = "no realizada"
            
            observaciones = tempDemanda.demandaObservaciones

            return render(request,"crm/saleDemanda.html",
                context={"id":demanda_id,
                        "contactoNombre":contactoNombre,
                        "contactoDni":contactoDNI,
                        "contactoEmail":contactoEmail,
                        "contactoTelefono":contactoTelefono,
                        "fechaRegistro":fechaRegistro,
                        "fechaEntrada":fechaEntrada,
                        "fechaSalida":fechaSalida,
                        "fechaAsignacion":fechaAsignacion,
                        "fechaVisita":fechaVisita,
                        "fechaOferta":fechaOferta
                        })

        elif request.method == "POST":
            now = datetime.now()
            dataPost = request.POST
            tempDemanda = claseDemanda.objects.get(demandaId=demanda_id)

            oferta = dataPost["oferta"]

            tempDemanda.demandaFOferta = now
            tempDemanda.demandaOferta = oferta
            tempDemanda.demandaHistAcciones = "[" + now.strftime("%d/%m/%Y %H:%M:%S") + "] [" + str(request.user) + "] Realizada nueva oferta por valor de: " + str(oferta) + " EUR/MES.||" + tempDemanda.demandaHistAcciones

            tempDemanda.save()

            url = "/crm/gestion-demanda/demanda/" + demanda_id + "/"
            return HttpResponseRedirect(url)
    else:
        return render(request,"noaccess.html")

@login_required
def  lostDemanda(request, demanda_id):
    if request.user.groups.filter(name="CRM").exists():
        if request.method == "GET":
            now = datetime.now()
            tempDemanda = claseDemanda.objects.get(demandaId=demanda_id)
            tempDemanda.demandaPerdida = True
            tempDemanda.demandaFCierre = now
            tempDemanda.demandaHistAcciones = "[" + now.strftime("%d/%m/%Y %H:%M:%S") +  "] [" + str(request.user) +"] Oportunidad perdida.||" + tempDemanda.demandaHistAcciones
            tempDemanda.save()

            url = "/crm/gestion-demanda"
            return HttpResponseRedirect(url)
    else:
        return render(request,"noaccess.html")

@login_required
def completeDemanda(request, demanda_id):
    if request.user.groups.filter(name="CRM").exists():
        if request.method == "GET":
            ## Iniciando variables
            now = datetime.now()
            tempDemanda = claseDemanda.objects.get(demandaId=demanda_id)
            tempContacto = claseContacto.objects.get(contactoDNI=tempDemanda.demandaContacto)

            # Datos del contacto
            contactoNombre = tempContacto.contactoNombre 
            contactoApellido = tempContacto.contactoApellido
            contactoDNI = tempContacto.contactoDNI
            contactoEmail = tempContacto.contactoEmail
            contactoTelefono = tempContacto.contactoTelefono

            # Fechas varias
            fechaRegistro = tempDemanda.demandaFRegistro.strftime("%d/%m/%Y")
            fechaEntrada = tempDemanda.demandaFEntrada.strftime("%d/%m/%Y")
            fechaSalida = tempDemanda.demandaFSalida.strftime("%d/%m/%Y")
            fechaAsignacion = tempDemanda.demandaFAsignacion.strftime("%d/%m/%Y")
            if tempDemanda.demandaFVisita != None:
                fechaVisita = tempDemanda.demandaFVisita.strftime("%d/%m/%Y")
            else:
                fechaVisita = "no realizada"
            if tempDemanda.demandaFOferta != None:
                fechaOferta =tempDemanda.demandaFOferta.strftime("%d/%m/%Y")
            else:
                fechaOferta = "no realizada"
            
            observaciones = tempDemanda.demandaObservaciones

            return render(request,"crm/completeDemanda.html",
                context={"id":demanda_id,
                        "contactoNombre":contactoNombre,
                        "contactoDni":contactoDNI,
                        "contactoEmail":contactoEmail,
                        "contactoTelefono":contactoTelefono,
                        "fechaRegistro":fechaRegistro,
                        "fechaEntrada":fechaEntrada,
                        "fechaSalida":fechaSalida,
                        "fechaAsignacion":fechaAsignacion,
                        "fechaVisita":fechaVisita,
                        "fechaOferta":fechaOferta
                        })

        elif request.method == "POST":
            now = datetime.now()
            tempDemanda = claseDemanda.objects.get(demandaId=demanda_id)
            tempDemanda.demandaGanada = True
            tempDemanda.demandaFCierre = now
            tempDemanda.demandaHistAcciones = "[" + now.strftime("%d/%m/%Y %H:%M:%S") + "] [" + str(request.user) + "] Oportunidad completada con éxito y convertida en reserva.||" + tempDemanda.demandaHistAcciones
            tempDemanda.save()

            tempComplete = request.POST
            if tempComplete["tipoPago"] == "1":
                fecha = tempDemanda.demandaFEntrada + timedelta(days=-1)
            elif tempComplete["tipoPago"] == "2":
                fecha = tempDemanda.demandaFEntrada + timedelta(days=-1)
            elif tempComplete["tipoPago"] == "3":
                fecha = tempDemanda.demandaFEntrada + timedelta(days=-1)
            elif tempComplete["tipoPago"] == "4":
                fecha = tempDemanda.demandaFEntrada + timedelta(days=-1)

            tempReserva = claseReserva.objects.create(
                demandaId = demanda_id,
                reservaContacto = tempDemanda.demandaContacto,
                reservaComercial = tempDemanda.demandaComercial,
                reservaApartamento = tempDemanda.demandaApartamento,
                reservaHabitacion = tempDemanda.demandaHabitacion,
                reservaFRegistro = now,
                reservaFEntrada = tempDemanda.demandaFEntrada,
                reservaFSalida = tempDemanda.demandaFSalida,
                reservaFPago = fecha,
                reservaFormaPago = tempComplete["formaPago"],
                reservaTipoPago = tempComplete["tipoPago"],
                reservaPago = tempDemanda.demandaOferta,
                reservaObservaciones = tempComplete["observaciones"],
                reservaHistAcciones = "[" + now.strftime("%d/%m/%Y %H:%M:%S") + "] [" + str(request.user) + "] Reserva registrada con éxito."
                )
            
            generarPagos(tempReserva.reservaId, tempDemanda.demandaFEntrada, tempDemanda.demandaFSalida, tempDemanda.demandaOferta, tempComplete["tipoPago"])

            url = "/pms/panel-de-reservas/reserva/" + str(tempReserva.reservaId)
            return HttpResponseRedirect(url)
    else:
        return render(request,"noaccess.html")

@login_required
def  calendarComercial(request):
    if request.user.groups.filter(name="CRM").exists():
        now = datetime.now() + timedelta(days=-1)
        listadoDemanda = claseDemanda.objects.order_by("demandaFVisita").filter(demandaFVisita__gte=now)
        visitas = []
        horas = []
        contactos = []

        for item in listadoDemanda:
            if item.demandaFVisita != None and item.demandaPerdida == False and item.demandaGanada == False:
                tempComercial = claseComercial.objects.get(comercialDNI=item.demandaComercial)
                item.demandaComercial = tempComercial.comercialNombre + " " + tempComercial.comercialApellido
                newHora = item.demandaFVisita.strftime("%H:%M")
                item.demandaFVisita = item.demandaFVisita.strftime("%d/%m/%Y")
                tempContacto = claseContacto.objects.get(contactoDNI=item.demandaContacto)
                newContacto = tempContacto.contactoNombre + " " + tempContacto.contactoApellido + " (" + tempContacto.contactoTelefono + ")"

                horas.append(newHora)
                visitas.append(item)
                contactos.append(newContacto)

        return render(request,"crm/calendarComercial.html",
                context={"visitas":visitas,
                            "horas":horas,
                            "contactos":contactos
                })
    else:
        return render(request,"noaccess.html")