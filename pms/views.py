from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import claseHabitacion, claseApartamento, clasePagos, claseVariables, claseReserva, claseTarjetas, claseCuentas, claseInquilinos
from crm.models import claseContacto, claseComercial, claseDemanda
from custom.habitaciones import getBanos, yesNo, getBed, getTipo, getUso
from custom.apartamentos import getAddress
from django.contrib.auth.decorators import login_required


import pandas as pd
import pytz
from datetime import datetime, timedelta

# Create your views here.
@login_required
def import_habitaciones(request):

    df = pd.read_csv("/home/mpilar/tfgsite/_importdata/habitaciones.csv")
    index = df.index
    n = len(index)
    html = ""
    for x in range (0, n):
        idhab = str(int(df.iloc[x].idhab))
        if len(idhab) == 1:
            idhab = "00" + idhab
        elif len(idhab) == 2:
            idhab = "0" + idhab

        idedif = str(int(df.iloc[x].idedif))
        if len(idedif) == 1:
            idedif = "0" + idedif

        identificador = "A" + idedif + "-HAB" + idhab

        metros = df.iloc[x].metros
        banos = int(df.iloc[x].banos)
        aseos = int(df.iloc[x].aseos)
        
        ventanas = df.iloc[x].ventanas
        if ventanas == 1:
            ventanas = True
        elif ventanas == 0:
            ventanas = False

        ascensor = df.iloc[x].ascensor
        if ascensor == 1:
            ascensor = True
        elif ascensor == 0:
            ascensor = False

        balcon = df.iloc[x].balcon
        if balcon == 1:
            balcon = True
        elif balcon == 0:
            balcon = False

        cama = str(int(df.iloc[x].cama))

        tipo = int(df.iloc[x].tipo)
        if tipo == 1:
            tipo = "INT"
        elif tipo == 0:
            tipo = "EXT"

        uso = int(df.iloc[x].uso)
        if uso == 1:
            uso = "IND"
        elif uso == 2:
            uso = "DOB"
    
        #h = claseHabitacion(name='Beatles Blog', tagline='All the latest Beatles news.')
        h = claseHabitacion(habitacionIdentificador = identificador, habitacionMetros = metros, habitacionBanos = banos, habitacionAseos = aseos, 
                                habitacionVentanas = ventanas, habitacionAscensor =ascensor, habitacionBalcon = balcon, habitacionCama = cama, 
                                habitacionTipo = tipo, habitacionUso = uso)
        h.save()
        html += str(identificador) + "<br>"
    
    return HttpResponse(html)

@login_required
def import_apartamentos(request):

    df = pd.read_csv("/home/mpilar/tfgsite/_importdata/apartamentos.csv")
    index = df.index
    n = len(index)
    html = ""
    for x in range (0, n):

        idedif = str(int(df.iloc[x].idedif))
        if len(idedif) == 1:
            idedif = "0" + idedif
        idedif = "A" + idedif

        calle = str(df.iloc[x].calle)
        numero = str(df.iloc[x].numero)
        piso = str(df.iloc[x].piso)
        letra = str(df.iloc[x].letra)
        ciudad = str(df.iloc[x].ciudad)
        estado = str(df.iloc[x].estado)
        pais = str(df.iloc[x].pais)
        cp = str(df.iloc[x].cp)
        otros = str(df.iloc[x].otros)

        a = claseApartamento(apartamentoIdentificador = idedif, apartamentoPais = pais, apartamentoEstado = estado, apartamentoCiudad = ciudad, apartamentoCalle = calle,
                                apartamentoNumero = numero, apartamentoPiso = piso, apartamentoLetra = letra, apartamentoCP = cp, apartamentoOtros = otros)
        a.save()
        html += str(idedif) + "<br>"
    
    return HttpResponse(html)

@login_required
def import_contactos(request):
    df = pd.read_excel(r"/home/mpilar/tfgsite/_importdata/importDemandas.xlsx", sheet_name="contactos")
    html = ""
    for pos in range (0, df.shape[0]):
        dni = str(df.iloc[pos]['dni'])
        nombre = str(df.iloc[pos]['nombre'])
        apellidos = str(df.iloc[pos]['apellidos'])
        email = str(df.iloc[pos]['email'])
        telefono = str(df.iloc[pos]['telefono'])

        new = claseContacto(contactoNombre = nombre, contactoApellido = apellidos, contactoEmail = email,
                                contactoTelefono = telefono, contactoDNI = dni)
        new.save()
        
        html += str(pos) + " | " + dni + " " + nombre + " " + apellidos + " " + email + " " + telefono + "<br>"

    return HttpResponse(html)

@login_required
def import_demandas(request):
    df = pd.read_excel(r"/home/mpilar/tfgsite/_importdata/importDemandas.xlsx", sheet_name="demandas")
    html = ""
    for pos in range (0, df.shape[0]):
        if not pd.isna(df.iloc[pos]['contacto']):
            contacto = str(df.iloc[pos]['contacto'])
            comercial = str(df.iloc[pos]['comercial'])
            apartamento = str(df.iloc[pos]['apartamento'])
            habitacion = str(df.iloc[pos]['habitacion'])
            fregistro = df.iloc[pos]['fregistro'] + datetime.timedelta(hours=2)
            fasignacion = df.iloc[pos]['fasignacion'] + datetime.timedelta(hours=2)
            fvisita = df.iloc[pos]['fvisita']
            foferta = df.iloc[pos]['foferta'] + datetime.timedelta(hours=2)
            oferta = int(df.iloc[pos]['oferta'])
            fentrada = df.iloc[pos]['fentrada'] + datetime.timedelta(hours=2)
            fsalida = df.iloc[pos]['fsalida'] + datetime.timedelta(hours=2)
            acciones = str(df.iloc[pos]['histacciones'])

            new = claseDemanda(demandaContacto = contacto, demandaComercial = comercial, demandaApartamento = apartamento, 
                                    demandaHabitacion = habitacion, demandaFRegistro = fregistro, demandaFAsignacion = fasignacion,
                                    demandaFVisita = fvisita, demandaFOferta = foferta, demandaOferta = oferta, demandaFEntrada = fentrada,
                                    demandaFSalida = fsalida, demandaHistAcciones = acciones
            )
            new.save()
            
            html += str(pos) + " | " + contacto + " " + comercial + " " + apartamento + " " + habitacion + "<br>"

    return HttpResponse(html)

@login_required
def listReservas(request):
    if request.user.groups.filter(name="PMS").exists():
        if request.method == "GET":        
            now = datetime.now()

            ########################
            # RESERVAS SIN EMPEZAR #
            ########################
            listadoReserva = claseReserva.objects.order_by("reservaFEntrada").filter(reservaFSalida__gte=now, reservaFEntrada__gte=now, reservaIniciada=False)

            total = 0
            for item in listadoReserva:
                total = total + 1
                contactoId = item.reservaContacto
                tempContacto = claseContacto.objects.get(contactoDNI=contactoId)
                item.reservaContacto = tempContacto.contactoNombre + " " + tempContacto.contactoApellido

                comercialId = item.reservaComercial
                if comercialId == 'none':
                    item.reservaComercial = 'No asignado'
                else:
                    tempComercial = claseComercial.objects.get(comercialDNI=comercialId)
                    item.reservaComercial = tempComercial.comercialNombre + " " + tempComercial.comercialApellido

                apartamentoId = item.reservaApartamento
                tempApartamento = claseApartamento.objects.get(apartamentoIdentificador=apartamentoId)
                item.reservaApartamento = tempApartamento.apartamentoIdentificador + " | " + tempApartamento.apartamentoCalle + " " + tempApartamento.apartamentoNumero + " " + tempApartamento.apartamentoPiso + tempApartamento.apartamentoLetra + " (" + tempApartamento.apartamentoCiudad + ")"
            
                fechaEntrada = item.reservaFEntrada
                item.reservaFEntrada = fechaEntrada.strftime("%d/%m/%Y")
                fechaSalida = item.reservaFSalida
                item.reservaFSalida = fechaSalida.strftime("%d/%m/%Y")            
                fechaPago = item.reservaFPago
                item.reservaFPago = fechaPago.strftime("%d/%m/%Y")

                if item.reservaTipoPago == "1":
                    item.reservaTipoPago = "Único"
                elif item.reservaTipoPago == "2":
                    item.reservaTipoPago = "Mensual"
                elif  item.reservaTipoPago == "3":
                    item.reservaTipoPago = "Trimestral"
                elif item.reservaFormaPago == "4":
                    item.reservaTipoPago = "Anual"

                if item.reservaFormaPago == "1":
                    item.reservaFormaPago = "Efectivo"
                elif item.reservaFormaPago == "2":
                    item.reservaFormaPago = "Tarjeta"
                elif  item.reservaFormaPago == "3":
                    item.reservaFormaPago = "Transferencia"

            ####################
            # RESERVAS ACTIVAS #
            ####################
            listadoReservaActiva = claseReserva.objects.order_by("reservaFEntrada").filter(reservaFEntrada__lte=now, reservaIniciada=True, reservaCompletada=False)

            totalActivas = 0
            for item in listadoReservaActiva:
                totalActivas = totalActivas + 1

                now_utc = pytz.utc.localize(now)
                # Actualizar fecha de pago
                item.reservaFPago = clasePagos.objects.filter(reservaId=item.reservaId, pagoCompletado=False).first()
                if item.reservaFPago != None:
                    item.reservaFPago = item.reservaFPago.pagoFecha
                    item.save()
                    if item.reservaFPago < now_utc:
                        item.reservaFPago = "<td class='text-danger'>" + item.reservaFPago.strftime("%d/%m/%Y") + "</td>"
                    else:
                        item.reservaFPago = "<td>" + item.reservaFPago.strftime("%d/%m/%Y") + "</td>"

                contactoId = item.reservaContacto
                tempContacto = claseContacto.objects.get(contactoDNI=contactoId)
                item.reservaContacto = tempContacto.contactoNombre + " " + tempContacto.contactoApellido

                comercialId = item.reservaComercial
                if comercialId == 'none':
                    item.reservaComercial = 'No asignado'
                else:
                    tempComercial = claseComercial.objects.get(comercialDNI=comercialId)
                    item.reservaComercial = tempComercial.comercialNombre + " " + tempComercial.comercialApellido

                apartamentoId = item.reservaApartamento
                tempApartamento = claseApartamento.objects.get(apartamentoIdentificador=apartamentoId)
                item.reservaApartamento = tempApartamento.apartamentoIdentificador + " | " + tempApartamento.apartamentoCalle + " " + tempApartamento.apartamentoNumero + " " + tempApartamento.apartamentoPiso + tempApartamento.apartamentoLetra + " (" + tempApartamento.apartamentoCiudad + ")"
            
                fechaEntrada = item.reservaFEntrada
                item.reservaFEntrada = fechaEntrada.strftime("%d/%m/%Y")
                if item.reservaFSalida.date() < now_utc.date():
                    item.reservaFSalida = "<td class='text-danger'>" + item.reservaFSalida.strftime("%d/%m/%Y") + "</td>"
                else:
                    item.reservaFSalida = "<td>" + item.reservaFSalida.strftime("%d/%m/%Y") + "</td>"       

                if item.reservaTipoPago == "1":
                    item.reservaTipoPago = "Único"
                elif item.reservaTipoPago == "2":
                    item.reservaTipoPago = "Mensual"
                elif  item.reservaTipoPago == "3":
                    item.reservaTipoPago = "Trimestral"
                elif item.reservaFormaPago == "4":
                    item.reservaTipoPago = "Anual"

                if item.reservaFormaPago == "1":
                    item.reservaFormaPago = "Efectivo"
                elif item.reservaFormaPago == "2":
                    item.reservaFormaPago = "Tarjeta"
                elif  item.reservaFormaPago == "3":
                    item.reservaFormaPago = "Transferencia"   
                elif item.reservaFormaPago == "4":
                    item.reservaFormaPago = "Domiciliación bancaria"
            
            #######################
            # RESERVAS PENDIENTES #
            #######################
            listadoReservaPendiente = claseReserva.objects.order_by("reservaFEntrada").filter(reservaFSalida__gte=now, reservaFEntrada__lte=now, reservaIniciada=False, reservaCompletada=False)

            totalPendiente = 0
            for item in listadoReservaPendiente:
                totalPendiente = totalPendiente + 1

                now_utc = pytz.utc.localize(now)
                # Actualizar fecha de pago
                item.reservaFPago = clasePagos.objects.filter(reservaId=item.reservaId, pagoCompletado=False).first()
                if item.reservaFPago != None:
                    item.reservaFPago = item.reservaFPago.pagoFecha
                    item.save()
                    if item.reservaFPago.date() < now_utc.date():
                        item.reservaFPago = "<td class='text-danger'>" + item.reservaFPago.strftime("%d/%m/%Y") + "</td>"
                    else:
                        item.reservaFPago = "<td>" + item.reservaFPago.strftime("%d/%m/%Y") + "</td>"

                contactoId = item.reservaContacto
                tempContacto = claseContacto.objects.get(contactoDNI=contactoId)
                item.reservaContacto = tempContacto.contactoNombre + " " + tempContacto.contactoApellido

                comercialId = item.reservaComercial
                if comercialId == 'none':
                    item.reservaComercial = 'No asignado'
                else:
                    tempComercial = claseComercial.objects.get(comercialDNI=comercialId)
                    item.reservaComercial = tempComercial.comercialNombre + " " + tempComercial.comercialApellido

                apartamentoId = item.reservaApartamento
                tempApartamento = claseApartamento.objects.get(apartamentoIdentificador=apartamentoId)
                item.reservaApartamento = tempApartamento.apartamentoIdentificador + " | " + tempApartamento.apartamentoCalle + " " + tempApartamento.apartamentoNumero + " " + tempApartamento.apartamentoPiso + tempApartamento.apartamentoLetra + " (" + tempApartamento.apartamentoCiudad + ")"
            
                if item.reservaFEntrada.date() <= now_utc.date():
                    item.reservaFEntrada = "<td class='text-danger'>" + item.reservaFEntrada.strftime("%d/%m/%Y") + "</td>"
                else:
                    item.reservaFEntrada = "<td>" + item.reservaFEntrada.strftime("%d/%m/%Y") + "</td>"
                fechaSalida = item.reservaFSalida
                item.reservaFSalida = fechaSalida.strftime("%d/%m/%Y")            

                if item.reservaTipoPago == "1":
                    item.reservaTipoPago = "Único"
                elif item.reservaTipoPago == "2":
                    item.reservaTipoPago = "Mensual"
                elif  item.reservaTipoPago == "3":
                    item.reservaTipoPago = "Trimestral"
                elif item.reservaFormaPago == "4":
                    item.reservaTipoPago = "Anual"

                if item.reservaFormaPago == "1":
                    item.reservaFormaPago = "Efectivo"
                elif item.reservaFormaPago == "2":
                    item.reservaFormaPago = "Tarjeta"
                elif  item.reservaFormaPago == "3":
                    item.reservaFormaPago = "Transferencia"   
                elif item.reservaFormaPago == "4":
                    item.reservaFormaPago = "Domiciliación bancaria"
            
            return render(request,"pms/listReserva.html",
            context={"reservas": listadoReserva,
                        "totReservas": total,
                        "activas": listadoReservaActiva,
                        "totActivas": totalActivas,
                        "pendientes":listadoReservaPendiente,
                        "totPendientes":totalPendiente
                        })
    else:
        return render(request,"noaccess.html")

@login_required
def showReserva(request, reserva_id):
    if request.user.groups.filter(name="PMS").exists():
        now = datetime.now()
        now_utc = pytz.utc.localize(now)
        # Recogiendo información de todas las bases de datos
        tempReserva = claseReserva.objects.get(reservaId=reserva_id)
        tempContacto = claseContacto.objects.get(contactoDNI=tempReserva.reservaContacto)
        tempPagos = clasePagos.objects.filter(reservaId=reserva_id)
        tempInquilinos = claseInquilinos.objects.filter(reservaId = reserva_id).order_by("-inquilinoTitular")
        tempApartamento = claseApartamento.objects.get(apartamentoIdentificador=tempReserva.reservaApartamento)
        tempHabitacion = claseHabitacion.objects.get(habitacionIdentificador=tempReserva.reservaHabitacion)

        # Actualizar fecha de pago
        tempPago = clasePagos.objects.filter(reservaId=reserva_id, pagoCompletado=False).first()
        if tempPago != None:
            tempReserva.reservaFPago = tempPago.pagoFecha
            tempReserva.save()
        if not tempReserva.reservaIniciada:
            checkin = "<button type=\"button\" class=\"btn btn-outline-success\" onclick=\"location.href='/pms/panel-de-reservas/reserva/" + str(tempReserva.reservaId) + "/checkin'\">Check In</button>"
        else:
            checkin = "<button type=\"button\" class=\"btn btn-outline-success\" onclick=\"location.href='/pms/panel-de-reservas/reserva/" + str(tempReserva.reservaId) + "/checkin'\" disabled>Check In</button>"
        
        if tempReserva.reservaFSalida.date() <= now_utc.date():
            fin = "<button type=\"button\" class=\"btn btn-outline-danger\" onclick=\"location.href='/pms/panel-de-reservas/reserva/" + str(tempReserva.reservaId) + "/complete'\">Finalizar</button>"
        else:
            fin = "<button type=\"button\" class=\"btn btn-outline-danger\" onclick=\"location.href='/pms/panel-de-reservas/reserva/" + str(tempReserva.reservaId) + "/complete'\" disabled>Finalizar</button>"
        
        if tempReserva.reservaFPago.date() <= now_utc.date():
            pago = "<button type=\"button\" class=\"btn btn-outline-primary\" onclick=\"location.href='/pms/panel-de-reservas/reserva/" + str(tempReserva.reservaId) + "/pay'\">Reg. Pago</button>"
        else:
            pago = "<button type=\"button\" class=\"btn btn-outline-primary\" onclick=\"location.href='/pms/panel-de-reservas/reserva/" + str(tempReserva.reservaId) + "/pay'\" disabled>Reg. Pago</button>"

        # Datos reserva
        if tempReserva.reservaFormaPago == "1":
            tempReserva.reservaFormaPago = "Efectivo"
        elif tempReserva.reservaFormaPago == "2":
            tempReserva.reservaFormaPago = "Tarjeta"
        elif tempReserva.reservaFormaPago == "3":
            tempReserva.reservaFormaPago = "Transferencia"

        if tempReserva.reservaTipoPago == "1":
            tempReserva.reservaTipoPago = "Único"
        elif tempReserva.reservaTipoPago == "2":
            tempReserva.reservaTipoPago = "Mensual"
        elif tempReserva.reservaTipoPago == "3":
            tempReserva.reservaTipoPago = "Trimestral"
        elif tempReserva.reservaTipoPago == "4":
            tempReserva.reservaTipoPago = "Anual"

        # Datos apartamento
        apartamentoDireccion = getAddress(tempApartamento)

        # Datos habitacion
        tempHabitacion.habitacionBanos = getBanos(tempHabitacion.habitacionBanos, tempHabitacion.habitacionAseos)
        tempHabitacion.habitacionVentanas = yesNo(tempHabitacion.habitacionVentanas)
        tempHabitacion.habitacionAscensor = yesNo(tempHabitacion.habitacionAscensor)
        tempHabitacion.habitacionBalcon = yesNo(tempHabitacion.habitacionBalcon)
        tempHabitacion.habitacionCama = getBed(tempHabitacion.habitacionCama)
        tempHabitacion.habitacionUso = getUso(tempHabitacion.habitacionUso)
        tempHabitacion.habitacionTipo = getTipo(tempHabitacion.habitacionTipo)
        
        # Datos del contacto
        contactoNombre = tempContacto.contactoNombre + " " + tempContacto.contactoApellido
        contactoDNI = tempContacto.contactoDNI
        contactoEmail = tempContacto.contactoEmail
        contactoTelefono = tempContacto.contactoTelefono

        # Datos de los pagos
        total = 0
        abonado = 0
        for item in tempPagos:
            total = total + 1

            if item.pagoCompletado:
                item.pagoCompletado = '<img src="/static/img/ok-icon.png" width="25" height="25" data-toggle="tooltip" title="Abonado">'
            else:
                if item.pagoFecha < now_utc:
                    item.pagoCompletado = '<img src="/static/img/danger-icon.png" width="25" height="25" data-toggle="tooltip" title="No pagado">'
                else:
                    item.pagoCompletado = '<img src="/static/img/info-icon.png" width="25" height="25" data-toggle="tooltip" title="Pendiente de pago">'

            item.pagoFecha = item.pagoFecha.strftime("%d/%m/%Y")
            item.pagoImporte = str(item.pagoImporte) + " EUR"
        
        if now_utc > tempReserva.reservaFPago:
            expired = True
        else:
            expired = False
        
        historico = tempReserva.reservaHistAcciones.split('||')

        return render(request,"pms/showReserva.html",
                context={"id":reserva_id,
                        "contactoNombre":contactoNombre,
                        "contactoDni":contactoDNI,
                        "contactoEmail":contactoEmail,
                        "contactoTelefono":contactoTelefono,
                        "apartamentoId":tempApartamento.apartamentoIdentificador,
                        "apartamentoDireccion":apartamentoDireccion,
                        "habitacionId":tempHabitacion.habitacionIdentificador,
                        "habitacionTamano":tempHabitacion.habitacionMetros,
                        "habitacionBanos":tempHabitacion.habitacionBanos,
                        "habitacionVentana":tempHabitacion.habitacionVentanas,
                        "habitacionAscensor":tempHabitacion.habitacionAscensor,
                        "habitacionBalcon":tempHabitacion.habitacionBalcon,
                        "habitacionCama":tempHabitacion.habitacionCama,
                        "habitacionOcupacion":tempHabitacion.habitacionUso,
                        "habitacionTipologia":tempHabitacion.habitacionTipo,
                        "formaPago":tempReserva.reservaFormaPago,
                        "plazoPago":tempReserva.reservaTipoPago,
                        "proximoPago":tempReserva.reservaFPago.strftime("%d/%m/%Y"),
                        "pagos":tempPagos,
                        "inquilinos":tempInquilinos,
                        "totInquilinos":len(tempInquilinos),
                        "total":total,
                        "abonado":abonado,
                        "expired":expired,
                        "checkin":checkin,
                        "end":fin,
                        "pay":pago,
                        "fechaEntrada":tempReserva.reservaFEntrada.strftime("%d/%m/%Y"),
                        "fechaSalida":tempReserva.reservaFSalida.strftime("%d/%m/%Y"),
                        "historico":historico
                        })
    else:
        return render(request,"noaccess.html")

@login_required
def checkinReserva(request, reserva_id):
    if request.user.groups.filter(name="PMS").exists():
        if request.method == "GET":
            # Recogiendo información de todas las bases de datos
            tempReserva = claseReserva.objects.get(reservaId=reserva_id)
            tempContacto = claseContacto.objects.get(contactoDNI=tempReserva.reservaContacto)
            tempApartamento = claseApartamento.objects.get(apartamentoIdentificador=tempReserva.reservaApartamento)
            tempHabitacion = claseHabitacion.objects.get(habitacionIdentificador=tempReserva.reservaHabitacion)

            domiciliacion = False
            tarjeta = False
            doble = False

            if tempReserva.reservaFormaPago == "4":
                domiciliacion = True
            elif tempReserva.reservaFormaPago == "2":
                tarjeta = True
            if tempHabitacion.habitacionUso == "DOB":
                doble = True
            
            return render(request,"pms/checkinReserva.html",
                    context={"id":reserva_id,
                            "contactoNombre":tempContacto.contactoNombre,
                            "contactoApellido":tempContacto.contactoApellido,
                            "contactoDni":tempContacto.contactoDNI,
                            "contactoEmail":tempContacto.contactoEmail,
                            "contactoTelefono":tempContacto.contactoTelefono,
                            "fechaEntrada":tempReserva.reservaFEntrada.strftime("%d/%m/%Y"),
                            "fechaSalida":tempReserva.reservaFSalida.strftime("%d/%m/%Y"),
                            "tarjeta":tarjeta,
                            "domiciliacion":domiciliacion,
                            "doble":doble
                            })

        elif request.method == "POST":
            now = datetime.now()
            tempReserva = claseReserva.objects.get(reservaId=reserva_id)
            tempHabitacion = claseHabitacion.objects.get(habitacionIdentificador=tempReserva.reservaHabitacion)
            if tempReserva.reservaFormaPago == "2":
                tarjetaNum = request.POST["numTarjeta"]
                tarjetaAno = request.POST["anoTarjeta"]
                tarjetaMes = request.POST["mesTarjeta"]
                tarjetaCVV = request.POST["cvvTarjeta"]
                tarjetaTitular = request.POST["titularTarjeta"]
                t = claseTarjetas(reservaId = reserva_id, tarjetaNum = tarjetaNum, tarjetaAno = tarjetaAno, tarjetaMes = tarjetaMes, tarjetaCVV = tarjetaCVV, tarjetaTitular = tarjetaTitular)
                t.save()
            elif tempReserva.reservaFormaPago == "4":
                cuentaTitular = request.POST["titularCuenta"]
                cuentaNum = request.POST["numCuenta"]
                c = claseCuentas(reservaId = reserva_id, cuentaNum = cuentaNum, cuentaTitular = cuentaTitular)
                c.save()
            if tempHabitacion.habitacionUso == "DOB":
                inquilinoNombre2 = request.POST["inquilinoNombre2"]
                inquilinoApellidos2 = request.POST["inquilinoApellido2"]
                inquilinoDni2 = request.POST["inquilinoDNI2"]
                i = claseInquilinos(reservaId = reserva_id, inquilinoNombre = inquilinoNombre2, inquilinoApellidos = inquilinoApellidos2, inquilinoDni = inquilinoDni2)
                i.save()

            inquilinoNombre1 = request.POST["inquilinoNombre1"]
            inquilinoApellidos1 = request.POST["inquilinoApellido1"]
            inquilinoDni1 = request.POST["inquilinoDNI1"]
            i = claseInquilinos(reservaId = reserva_id, inquilinoNombre = inquilinoNombre1, inquilinoApellidos = inquilinoApellidos1, inquilinoDni = inquilinoDni1, inquilinoTitular = True)
            i.save()

            tempReserva.reservaHistAcciones = "[" + now.strftime("%d/%m/%Y %H:%M:%S") + "] [" + str(request.user) + "] Check-In realizado.||" + tempReserva.reservaHistAcciones
            tempReserva.reservaIniciada = True
            tempReserva.save()

            url = "/pms/panel-de-reservas"
            return redirect(url)
    else:
        return render(request,"noaccess.html")

@login_required
def payReserva(request, reserva_id):
    if request.user.groups.filter(name="PMS").exists():
        now = datetime.now()

        tempReserva = claseReserva.objects.get(reservaId=reserva_id)
        tempReserva.reservaHistAcciones = "[" + now.strftime("%d/%m/%Y %H:%M:%S") + "] [" + str(request.user) + "] Pago registrado.||" + tempReserva.reservaHistAcciones
        tempReserva.save()

        tempPagos = clasePagos.objects.filter(reservaId=reserva_id, pagoCompletado=False).first()
        tempPagos.pagoCompletado = True
        tempPagos.save()

        url = "/pms/panel-de-reservas/reserva/" + str(reserva_id)
        return redirect(url)
    else:
        return render(request,"noaccess.html")

@login_required
def completeReserva(request, reserva_id):
    if request.user.groups.filter(name="PMS").exists():
        tempReserva = claseReserva.objects.get(reservaId=reserva_id)
        tempReserva.reservaCompletada = True
        tempReserva.save()
        url = "/pms/panel-de-reservas"
        return redirect(url)
    else:
        return render(request,"noaccess.html")

@login_required
def checkinPanel(request):
    if request.user.groups.filter(name="PMS").exists():
        now = datetime.now()
        tomorrow = now + timedelta(hours=24)
        #######################
        # RESERVAS PENDIENTES #
        #######################
        listadoReservasHoy = claseReserva.objects.order_by("reservaFEntrada").filter(reservaFEntrada__gte=now.replace(hour=0,minute=0,second=0), reservaFEntrada__lt=tomorrow.replace(hour=0,minute=0,second=0), reservaIniciada=False, reservaCompletada=False)

        
        for item in listadoReservasHoy:

            now_utc = pytz.utc.localize(now)
            # Actualizar fecha de pago
            item.reservaFPago = clasePagos.objects.filter(reservaId=item.reservaId, pagoCompletado=False).first()
            item.reservaFPago = item.reservaFPago.pagoFecha
            item.save()

            contactoId = item.reservaContacto
            tempContacto = claseContacto.objects.get(contactoDNI=contactoId)
            item.reservaContacto = tempContacto.contactoNombre + " " + tempContacto.contactoApellido

            comercialId = item.reservaComercial
            if comercialId == 'none':
                item.reservaComercial = 'No asignado'
            else:
                tempComercial = claseComercial.objects.get(comercialDNI=comercialId)
                item.reservaComercial = tempComercial.comercialNombre + " " + tempComercial.comercialApellido

            apartamentoId = item.reservaApartamento
            tempApartamento = claseApartamento.objects.get(apartamentoIdentificador=apartamentoId)
            item.reservaApartamento = tempApartamento.apartamentoIdentificador + " | " + tempApartamento.apartamentoCalle + " " + tempApartamento.apartamentoNumero + " " + tempApartamento.apartamentoPiso + tempApartamento.apartamentoLetra + " (" + tempApartamento.apartamentoCiudad + ")"
        
            item.reservaFEntrada = item.reservaFEntrada.strftime("%d/%m/%Y") 
            item.reservaFSalida = item.reservaFSalida.strftime("%d/%m/%Y")          
            item.reservaFPago = item.reservaFPago.strftime("%d/%m/%Y")          

            if item.reservaTipoPago == "1":
                item.reservaTipoPago = "Único"
            elif item.reservaTipoPago == "2":
                item.reservaTipoPago = "Mensual"
            elif  item.reservaTipoPago == "3":
                item.reservaTipoPago = "Trimestral"
            elif item.reservaFormaPago == "4":
                item.reservaTipoPago = "Anual"

            if item.reservaFormaPago == "1":
                item.reservaFormaPago = "Efectivo"
            elif item.reservaFormaPago == "2":
                item.reservaFormaPago = "Tarjeta"
            elif  item.reservaFormaPago == "3":
                item.reservaFormaPago = "Transferencia"   
            elif item.reservaFormaPago == "4":
                item.reservaFormaPago = "Domiciliación bancaria"

        return render(request,"pms/checkinPanel.html",
                        context={
                            "reservas":listadoReservasHoy,
                            "totReservas":len(listadoReservasHoy)
                        })
    else:
        return render(request,"noaccess.html")

@login_required
def herramienta_calculadora(request):
    if request.user.groups.filter(name="PMS").exists():
        tempVariables = claseVariables.objects.get(id=1)

        # Variables TIPO
        tipoInt = tempVariables.varCalculadoraTipoInt
        tipoExt = tempVariables.varCalculadoraTipoExt

        # Variables USO
        usoInd = tempVariables.varCalculadoraUsoInd
        usoDob = tempVariables.varCalculadoraUsoDob

        return render(request,"pms/toolsCalculadora.html",
            context={"tipoInt":tipoInt,
                        "tipoExt":tipoExt,
                        "usoInd":usoInd,
                        "usoDob":usoDob,
            }
        )
    else:
        return render(request,"noaccess.html")

@login_required
def planningOcupacion(request):
    
    if request.user.groups.filter(name="PMS").exists():
        if request.method == "GET":
            now = datetime.now()
            month = now.month
            year = now.year

            listMonth = []
            for x in range(12):
                temp = 1 + x
                if temp > 12:
                    temp = temp - 12
                listMonth.append(temp)
            
            listYear = [year-2, year-1]
            for x in range(5):
                temp = year + x
                listYear.append(temp)

            listApartments = claseApartamento.objects.all()
            
            return render(request,"pms/listPlanning.html",
            context={"show":False,
                        "months":listMonth,
                        "month":month,
                        "years":listYear,
                        "year":year,
                        "apartments":listApartments
            }
        )

        elif request.method == "POST":
            now = datetime.now()

            apartment = request.POST["apartment"]
            month = int(request.POST["month"])
            year = int(request.POST["year"])

            if month == 1:
                prevMonth = 12
                prevYear = year-1
            else:
                prevMonth = month-1
                prevYear = year
            
            if month == 12:
                nextMonth = 1
                nextYear = year + 1
            else:
                nextMonth = month + 1
                nextYear = year

            firstDay = datetime(year, month, 1)
            listRooms = claseHabitacion.objects.filter(habitacionIdentificador__startswith=apartment)
            
            dataControl = 12 # Meses
            if month in [1, 3, 5, 7, 8, 10, 12]:
                days = 31
            elif month in [4, 6, 9, 11]:
                days = 30
            elif month in [2]:
                days = 28
            listDays = []
            for x in range(days):
                listDays.append(x+1)

            roomsAvailability = []
            for room in listRooms:
                list = [0] * days
                listAnterior = claseReserva.objects.filter(reservaHabitacion=room.habitacionIdentificador,reservaFEntrada__lte=firstDay).order_by("-reservaFEntrada").last()
                for x in range(len(list)):
                    caso1 = False
                    caso2 = False
                    today = datetime(year, month, x+1)
                    if listAnterior != None:
                        enterDate = datetime(listAnterior.reservaFEntrada.year, listAnterior.reservaFEntrada.month, listAnterior.reservaFEntrada.day)
                        exitDate = datetime(listAnterior.reservaFSalida.year, listAnterior.reservaFSalida.month, listAnterior.reservaFSalida.day)
                        if enterDate < today and exitDate > today:
                            list[x] = 1
                roomsAvailability.append(list)
            
                listActual = claseReserva.objects.filter(reservaHabitacion=room.habitacionIdentificador,reservaFEntrada__month=month, reservaFEntrada__year=year)
                for item in listActual:
                    for x in range(len(list)):
                        if x+1 < item.reservaFEntrada.day:
                            list[x] = 0
                        elif x+1 > item.reservaFSalida.day:
                            list[x] = 0
                        else:
                            list[x] = 1
   
            # Preparando plantilla html
            listMonth = []
            for x in range(12):
                temp = 1 + x
                if temp > 12:
                    temp = temp - 12
                listMonth.append(temp)
            
            listYear = [now.year-2, now.year-1]
            for x in range(5):
                temp = now.year + x
                listYear.append(temp)

            listApartments = claseApartamento.objects.all()
            
            return render(request,"pms/listPlanning.html",
            context={"show":True,
                        "months":listMonth,
                        "month":month,
                        "prevMonth":prevMonth,
                        "nextMonth":nextMonth,
                        "years":listYear,
                        "year":year,
                        "prevYear":prevYear,
                        "nextYear":nextYear,
                        "apartments":listApartments,
                        "apartment":apartment,
                        "roomsAvailability":roomsAvailability,
                        "listRooms":listRooms,
                        "days":listDays
            }
        )
    else:
        return render(request,"noaccess.html")