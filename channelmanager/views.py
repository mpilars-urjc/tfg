from pms.models import claseApartamento, claseHabitacion, claseVariables
from crm.models import claseComercial, claseDemanda
from custom.apartamentos import getAddress
from custom.habitaciones import getBed, getBanos, getUso, getTipo, yesNo
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from datetime import datetime

import locale

# Create your views here.
@login_required
def  listInmuebles(request):
    if request.user.groups.filter(name="Channel Manager").exists():
        if request.method == "GET":
            listadoApartamento = claseApartamento.objects.order_by("apartamentoIdentificador")
            listadoHabitacion = claseHabitacion.objects.order_by("habitacionIdentificador")
            apartamentos = []
            direcciones = []
            habitaciones = []
            otros = []

            for item in listadoApartamento:
                apartamentoDireccion = getAddress(item)
                count = 0
                for room in listadoHabitacion:
                    if room.habitacionIdentificador[:3] == item.apartamentoIdentificador:
                        count = count + 1
                apartamentos.append(item.apartamentoIdentificador)
                direcciones.append(apartamentoDireccion)
                habitaciones.append(count)
                if item.apartamentoOtros != "nan":
                    otros.append(item.apartamentoOtros)
                else:
                    otros.append("")           
                
            return render(request,"channelmanager/listInmuebles.html",
            context={"apartamentos": apartamentos,
                        "direcciones":direcciones,
                        "habitaciones":habitaciones,
                        "otros":otros
            })
    else:
        return render(request,"noaccess.html")

@login_required
def  showInmueble(request, apartamento_id):
    if request.user.groups.filter(name="Channel Manager").exists():
        if request.method == "GET":
            # Recogiendo información de todas las bases de datos
            tempApartamento = claseApartamento.objects.get(apartamentoIdentificador=apartamento_id)
            tempHabitacion = claseHabitacion.objects.filter(habitacionIdentificador__startswith=apartamento_id)

            # Datos apartamento
            apartamentoId = apartamento_id
            apartamentoDireccion = getAddress(tempApartamento)
            apartamentoHabitaciones = len(tempHabitacion)
            apartamentoFAlta = tempApartamento.apartamentoFechaDeAlta.strftime("%d/%m/%Y")

            # Datos habitacion
            for item in tempHabitacion:
                item.habitacionBanos = getBanos(item.habitacionBanos, item.habitacionAseos)
                item.habitacionVentanas = yesNo(item.habitacionVentanas)
                item.habitacionAscensor = yesNo(item.habitacionAscensor)
                item.habitacionBalcon = yesNo(item.habitacionBalcon)
                item.habitacionCama = getBed(item.habitacionCama)
                item.habitacionUso = getUso(item.habitacionUso)
                item.habitacionTipo = getTipo(item.habitacionTipo)
                

            return render(request,"channelmanager/showInmueble.html",
                    context={"id":apartamento_id,
                            "apartamentoId":apartamentoId,
                            "apartamentoDireccion":apartamentoDireccion,
                            "apartamentoHabitaciones":apartamentoHabitaciones,
                            "apartamentoFAlta":apartamentoFAlta,
                            "habitaciones":tempHabitacion
                            })
    else:
        return render(request,"noaccess.html")

@login_required
def newInmueble(request):
    if request.user.groups.filter(name="Channel Manager").exists():
        if request.method == "GET":
            return render(request,"channelmanager/newInmueble.html")

        elif request.method == "POST":
            dataPost = request.POST
            obj = claseApartamento.objects.latest('id')

            p = claseApartamento.objects.create(
                apartamentoIdentificador = "A" + str(int(obj.apartamentoIdentificador[1:]) + 1),
                apartamentoPais = dataPost["inmPais"],
                apartamentoEstado = dataPost["inmEstado"],
                apartamentoCiudad = dataPost["inmCiudad"],
                apartamentoCalle = dataPost["inmVia"] + " " + dataPost["inmCalle"],
                apartamentoNumero = dataPost["inmNumero"],
                apartamentoPiso = dataPost["inmPiso"],
                apartamentoLetra = dataPost["inmLetra"],
                apartamentoCP = dataPost["inmCP"],
                apartamentoOtros = dataPost["inmOtros"],
                apartamentoFechaDeAlta = datetime.now()
            )

            p.save()

            url = "/channelmanager/gestion-de-inmuebles/inmueble/" + str(p.apartamentoIdentificador)
            return redirect(url)
    else:
        return render(request,"noaccess.html")

@login_required
def deleteInmueble(request):
    if request.user.groups.filter(name="Channel Manager").exists():
        if request.method == "GET":
            # Recogiendo información de todas las bases de datos
            tempApartamento = claseApartamento.objects.order_by("apartamentoIdentificador")

            return render(request,"channelmanager/deleteInmueble.html",
                            context={"listadoApartamentos":tempApartamento
                            })

        if request.method == "POST":
            id = request.POST["apart"]
            tempApartamento = claseApartamento.objects.filter(apartamentoIdentificador=id)
            tempHabitacion = claseHabitacion.objects.filter(habitacionIdentificador__startswith=id)

            for item in tempHabitacion:
                claseHabitacion.objects.filter(habitacionIdentificador=item.habitacionIdentificador).delete()
            
            claseApartamento.objects.filter(apartamentoIdentificador=id).delete()

            url = "/channelmanager/gestion-de-inmuebles"
            return redirect(url)
    else:
        return render(request,"noaccess.html")

@login_required
def newRoom(request, apartamento_id):
    if request.user.groups.filter(name="Channel Manager").exists():
        if request.method == "GET":
            tempApartamento = claseApartamento.objects.get(apartamentoIdentificador=apartamento_id)
            tempHabitacion = claseHabitacion.objects.filter(habitacionIdentificador__startswith=apartamento_id)
            apartamentoHabitaciones = len(tempHabitacion)
            direccion = getAddress(tempApartamento)
            banos = tempHabitacion[0].habitacionBanos
            aseos = tempHabitacion[0].habitacionAseos
            ascensor = yesNo(tempHabitacion[0].habitacionAscensor)
            return render(request,"channelmanager/newRoom.html",
                            context={"apartamentoDireccion":direccion,
                                        "id":apartamento_id,
                                        "apartamentoFAlta":tempApartamento.apartamentoFechaDeAlta.strftime("%d/%m/%Y"),
                                        "apartamentoHabitaciones":apartamentoHabitaciones,
                                        "banos":banos,
                                        "aseos":aseos,
                                        "ascensor":ascensor
                            })
        
        elif request.method == "POST":
            dataPost = request.POST
            tempApartamento = claseApartamento.objects.get(apartamentoIdentificador=apartamento_id)
            tempHabitacion = claseHabitacion.objects.filter(habitacionIdentificador__startswith=apartamento_id)
            obj = tempHabitacion.latest('id').habitacionIdentificador
            apartamentoHabitaciones = len(tempHabitacion)
            if apartamentoHabitaciones == 0:
                habitacionIdentificador = str(apartamento_id) + "-HAB001"
            elif apartamentoHabitaciones < 10:
                habitacionIdentificador = str(apartamento_id) + "-HAB00" + str(int(obj[7:]) + 1)
            elif apartamentoHabitaciones < 100:
                habitacionIdentificador = str(apartamento_id) + "-HAB0" + str(int(obj[7:]) + 1)
            else:
                habitacionIdentificador = str(apartamento_id) + "-HAB" + str(int(obj[7:]) + 1)

            p = claseHabitacion.objects.create(
                habitacionIdentificador = habitacionIdentificador,
                habitacionMetros = dataPost["habTamano"],
                habitacionBanos = dataPost["habBanos"],
                habitacionAseos = dataPost["habAseos"],
                habitacionVentanas = dataPost["habVentana"],
                habitacionAscensor = dataPost["habAscensor"],
                habitacionBalcon = dataPost["habBalcon"],
                habitacionCama = dataPost["habCama"],
                habitacionTipo = dataPost["habTipo"],
                habitacionUso = dataPost["habUso"],
                habitacionFechaDeAlta = datetime.now()
            )

            p.save()

            url = "/channelmanager/gestion-de-inmuebles/inmueble/" + str(apartamento_id)
            return redirect(url)
    else:
        return render(request,"noaccess.html")

@login_required
def deleteRoom(request, apartamento_id):
    if request.user.groups.filter(name="Channel Manager").exists():
        if request.method == "GET":
            tempApartamento = claseApartamento.objects.get(apartamentoIdentificador=apartamento_id)
            tempHabitacion = claseHabitacion.objects.filter(habitacionIdentificador__startswith=apartamento_id)
            apartamentoHabitaciones = len(tempHabitacion)
            direccion = getAddress(tempApartamento)

            # Datos habitacion
            for item in tempHabitacion:
                item.habitacionBanos = getBanos(item.habitacionBanos, item.habitacionAseos)
                item.habitacionVentanas = yesNo(item.habitacionVentanas)
                item.habitacionAscensor = yesNo(item.habitacionAscensor)
                item.habitacionBalcon = yesNo(item.habitacionBalcon)
                item.habitacionCama = getBed(item.habitacionCama)
                item.habitacionUso = getUso(item.habitacionUso)
                item.habitacionTipo = getTipo(item.habitacionTipo)

            return render(request,"channelmanager/deleteRoom.html",
                            context={"apartamentoDireccion":direccion,
                                        "id":apartamento_id,
                                        "apartamentoFAlta":tempApartamento.apartamentoFechaDeAlta.strftime("%d/%m/%Y"),
                                        "apartamentoHabitaciones":apartamentoHabitaciones,
                                        "listadoHabitaciones":tempHabitacion
                            })

        elif request.method == "POST":
            id = request.POST["hab"]
            claseHabitacion.objects.filter(habitacionIdentificador=id).delete()
            url = "/channelmanager/gestion-de-inmuebles/inmueble/" + str(apartamento_id)
            return redirect(url)
    else:
        return render(request,"noaccess.html")

@login_required
def  listComerciales(request):
    if request.user.groups.filter(name="Channel Manager").exists():
        if request.method == "GET":
            listadoComerciales = claseComercial.objects.order_by("comercialDNI")
            activas = []
            ganadas = []
            perdidas = []
            total = []

            for item in listadoComerciales:
                item.comercialFechaDeAlta =  item.comercialFechaDeAlta.strftime("%d/%m/%Y")
                tempDemanda = claseDemanda.objects.filter(demandaComercial=item.comercialDNI, demandaPerdida=False, demandaGanada=False)
                activas.append(len(tempDemanda))
                tempDemanda = claseDemanda.objects.filter(demandaComercial=item.comercialDNI, demandaGanada=True)
                ganadas.append(len(tempDemanda))
                tempDemanda = claseDemanda.objects.filter(demandaComercial=item.comercialDNI, demandaPerdida=True)
                perdidas.append(len(tempDemanda))
                tempDemanda = claseDemanda.objects.filter(demandaComercial=item.comercialDNI)
                total.append(len(tempDemanda))

            return render(request,"channelmanager/listComerciales.html",
            context={"comerciales":listadoComerciales,
                        "activas":activas,
                        "ganadas":ganadas,
                        "perdidas":perdidas,
                        "total":total
            })
    else:
        return render(request,"noaccess.html")

@login_required
def disableComerciales(request, comercial_id):
    if request.user.groups.filter(name="Channel Manager").exists():
        disableComercial = claseComercial.objects.get(comercialDNI=comercial_id)
        disableComercial.comercialActivo = False
        disableComercial.save()

        url = "/channelmanager/gestion-de-comerciales"
        return redirect(url)
    else:
        return render(request,"noaccess.html")

@login_required
def enableComerciales(request, comercial_id):
    if request.user.groups.filter(name="Channel Manager").exists():
        enableComercial = claseComercial.objects.get(comercialDNI=comercial_id)
        enableComercial.comercialActivo = True
        enableComercial.save()

        url = "/channelmanager/gestion-de-comerciales"
        return redirect(url)
    else:
        return render(request,"noaccess.html")

@login_required
def showComerciales(request, comercial_id):
    if request.user.groups.filter(name="Channel Manager").exists():
        tempComercial = claseComercial.objects.get(comercialDNI=comercial_id)
        tempComercial.comercialFechaDeAlta = tempComercial.comercialFechaDeAlta.strftime("%d/%m/%Y")
        tempComercial.comercialActivo = yesNo(tempComercial.comercialActivo)

        tempDemanda = claseDemanda.objects.filter(demandaComercial=comercial_id).order_by("-demandaFRegistro")
        for item in tempDemanda:
            item.demandaFRegistro = item.demandaFRegistro.strftime("%d/%m/%Y")
            item.demandaFEntrada = item.demandaFEntrada.strftime("%d/%m/%Y")
            item.demandaFSalida = item.demandaFSalida.strftime("%d/%m/%Y")
            item.demandaPerdida = yesNo(item.demandaPerdida)
            item.demandaGanada = yesNo(item.demandaGanada)
        
        num = len(tempDemanda)

        return render(request,"channelmanager/showComercial.html",
            context={"comercial":tempComercial,
                        "demandas":tempDemanda,
                        "num":num
            })
    else:
        return render(request,"noaccess.html")

@login_required
def newComerciales(request):
    if request.user.groups.filter(name="Channel Manager").exists():
        if request.method == "GET":
            return render(request,"channelmanager/newComercial.html")

        elif request.method == "POST":
            p = claseComercial.objects.create(
                comercialNombre = request.POST["comNombre"],
                comercialApellido = request.POST["comApellidos"],
                comercialDNI = request.POST["comDNI"],
                comercialActivo = True
            )
            p.save()

            url = "/channelmanager/gestion-de-comerciales"
            return redirect(url)
    else:
        return render(request,"noaccess.html")

@login_required
def editVariables(request):
    if request.user.groups.filter(name="Channel Manager").exists():
        if request.method == "GET":
            tempVariables = claseVariables.objects.get()
            varCalculadoraTipoInt = tempVariables.varCalculadoraTipoInt * 100
            varCalculadoraTipoExt = tempVariables.varCalculadoraTipoExt * 100
            varCalculadoraUsoInd = tempVariables.varCalculadoraUsoInd * 100
            varCalculadoraUsoDob = tempVariables.varCalculadoraUsoDob * 100
            varCalculadoraHab4 = tempVariables.varCalculadoraHab4 * 100
            varCalculadoraHab5 = tempVariables.varCalculadoraHab5 * 100
            varCalculadoraHab6 = tempVariables.varCalculadoraHab6 * 100
            varCalculadoraHab7 = tempVariables.varCalculadoraHab7 * 100
            varCalculadoraHab8 = tempVariables.varCalculadoraHab8 * 100
            varCalculadoraHabPlus = tempVariables.varCalculadoraHabPlus * 100
            varCalculadoraBalSi = tempVariables.varCalculadoraBalSi * 100
            varCalculadoraBalNo = tempVariables.varCalculadoraBalNo * 100
            varCalculadoraAscSi = tempVariables.varCalculadoraAscSi * 100
            varCalculadoraAscNo = tempVariables.varCalculadoraAscNo * 100
            varCalculadoraCama90 = tempVariables.varCalculadoraCama90 * 100
            varCalculadoraCama105 = tempVariables.varCalculadoraCama105 * 100
            varCalculadoraCama135 = tempVariables.varCalculadoraCama135 * 100
            varCalculadoraCama150 = tempVariables.varCalculadoraCama150 * 100
            varCalculadoraCama2x90 = tempVariables.varCalculadoraCama2x90 * 100
            varCalculadoraZona1 = tempVariables.varCalculadoraZona1 * 100
            varCalculadoraZona2 = tempVariables.varCalculadoraZona2 * 100
            varCalculadoraZona3 = tempVariables.varCalculadoraZona3 * 100

            return render(request, "channelmanager/editVariables.html",
                            context={
                                "varCalculadoraTipoInt":int(varCalculadoraTipoInt),
                                "varCalculadoraTipoExt":int(varCalculadoraTipoExt),
                                "varCalculadoraUsoInd":int(varCalculadoraUsoInd),
                                "varCalculadoraUsoDob":int(varCalculadoraUsoDob),
                                "varCalculadoraBalSi":int(varCalculadoraBalSi),
                                "varCalculadoraBalNo":int(varCalculadoraBalNo),
                                "varCalculadoraAscSi":int(varCalculadoraAscSi),
                                "varCalculadoraAscNo":int(varCalculadoraAscNo),
                                "varCalculadoraHab4":int(varCalculadoraHab4),
                                "varCalculadoraHab5":int(varCalculadoraHab5),
                                "varCalculadoraHab6":int(varCalculadoraHab6),
                                "varCalculadoraHab7":int(varCalculadoraHab7),
                                "varCalculadoraHab8":int(varCalculadoraHab8),
                                "varCalculadoraHabPlus":int(varCalculadoraHabPlus),
                                "varCalculadoraCama90":int(varCalculadoraCama90),
                                "varCalculadoraCama105":int(varCalculadoraCama105),
                                "varCalculadoraCama135":int(varCalculadoraCama135),
                                "varCalculadoraCama150":int(varCalculadoraCama150),
                                "varCalculadoraCama2x90":int(varCalculadoraCama2x90),
                                "varCalculadoraZona1":int(varCalculadoraZona1),
                                "varCalculadoraZona2":int(varCalculadoraZona2),
                                "varCalculadoraZona3":int(varCalculadoraZona3),
            })

        elif request.method == "POST":

            tempVariables = request.POST
            varCalculadoraTipoInt = int(tempVariables["varCalculadoraTipoInt"]) / 100
            varCalculadoraTipoExt = int(tempVariables["varCalculadoraTipoExt"]) / 100
            varCalculadoraUsoInd = int(tempVariables["varCalculadoraUsoInd"]) / 100
            varCalculadoraUsoDob = int(tempVariables["varCalculadoraUsoDob"]) / 100
            varCalculadoraHab4 = int(tempVariables["varCalculadoraHab4"]) / 100
            varCalculadoraHab5 = int(tempVariables["varCalculadoraHab5"]) / 100
            varCalculadoraHab6 = int(tempVariables["varCalculadoraHab6"]) / 100
            varCalculadoraHab7 = int(tempVariables["varCalculadoraHab7"]) / 100
            varCalculadoraHab8 = int(tempVariables["varCalculadoraHab8"]) / 100
            varCalculadoraHabPlus = int(tempVariables["varCalculadoraHabPlus"]) / 100
            varCalculadoraBalSi = int(tempVariables["varCalculadoraBalSi"]) / 100
            varCalculadoraBalNo = int(tempVariables["varCalculadoraBalNo"]) / 100
            varCalculadoraAscSi = int(tempVariables["varCalculadoraAscSi"]) / 100
            varCalculadoraAscNo = int(tempVariables["varCalculadoraAscNo"]) / 100
            varCalculadoraCama90 = int(tempVariables["varCalculadoraCama90"]) / 100
            varCalculadoraCama105 = int(tempVariables["varCalculadoraCama105"]) / 100
            varCalculadoraCama135 = int(tempVariables["varCalculadoraCama135"]) / 100
            varCalculadoraCama150 = int(tempVariables["varCalculadoraCama150"]) / 100
            varCalculadoraCama2x90 = int(tempVariables["varCalculadoraCama2x90"]) / 100
            varCalculadoraZona1 = int(tempVariables["varCalculadoraZona1"]) / 100
            varCalculadoraZona2 = int(tempVariables["varCalculadoraZona2"]) / 100
            varCalculadoraZona3 = int(tempVariables["varCalculadoraZona3"]) / 100

            p = claseVariables.objects.get()
            p.varCalculadoraTipoInt = varCalculadoraTipoInt
            p.varCalculadoraTipoExt = varCalculadoraTipoExt
            p.varCalculadoraUsoInd = varCalculadoraUsoInd
            p.varCalculadoraUsoDob = varCalculadoraUsoDob
            p.varCalculadoraHab4 = varCalculadoraHab4
            p.varCalculadoraHab5 = varCalculadoraHab5
            p.varCalculadoraHab6 = varCalculadoraHab6
            p.varCalculadoraHab7 = varCalculadoraHab7
            p.varCalculadoraHab8 = varCalculadoraHab8
            p.varCalculadoraHabPlus = varCalculadoraHabPlus
            p.varCalculadoraBalSi = varCalculadoraBalSi
            p.varCalculadoraBalNo = varCalculadoraBalNo
            p.varCalculadoraAscSi = varCalculadoraAscSi
            p.varCalculadoraAscNo = varCalculadoraAscNo
            p.varCalculadoraCama90 = varCalculadoraCama90
            p.varCalculadoraCama105 = varCalculadoraCama105
            p.varCalculadoraCama135 = varCalculadoraCama135
            p.varCalculadoraCama150 = varCalculadoraCama150
            p.varCalculadoraCama2x90 = varCalculadoraCama2x90
            p.varCalculadoraZona1 = varCalculadoraZona1
            p.varCalculadoraZona2 = varCalculadoraZona2
            p.varCalculadoraZona3 = varCalculadoraZona3
            p.save()
            
            url = "/channelmanager/gestion-de-variables"
            return redirect(url)
    else:
        return render(request,"noaccess.html")