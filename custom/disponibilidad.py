from pms.models import claseReserva
from crm.models import claseDemanda

def check(start, end, room, id):
    listadoReserva = claseReserva.objects.order_by("reservaFEntrada").filter(reservaHabitacion=room)
    listadoDemanda = claseDemanda.objects.order_by("demandaFEntrada").filter(demandaHabitacion=room, demandaPerdida=False, demandaGanada=False).exclude(demandaId=id)

    val = -1
    existReserva = False
    existDemanda = False

    for item in listadoReserva:
        if (start < item.reservaFEntrada and end < item.reservaFEntrada) or (start > item.reservaFSalida and end > item.reservaFSalida):
            None
        else:
            existReserva = True

    for item in listadoDemanda:
        if (start < item.demandaFEntrada and end < item.demandaFEntrada) or (start > item.demandaFSalida and end > item.demandaFSalida):
            None
        else:
            existDemanda = True
    
    if existReserva and existDemanda:
        val = 2
    elif existReserva and not existDemanda:
        val = 2
    elif not existReserva and existDemanda:
        val = 1
    elif not existReserva and not existDemanda:
        val = 0
    
    return val