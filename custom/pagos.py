from pms.models import clasePagos
from math import ceil
from datetime import timedelta

def generarPagos (numReserva, fechaInicio, fechaFin, importe, formaPago):
    estancia = fechaFin - fechaInicio
    meses = ceil(estancia.days/30)
    if formaPago == "1":
        numeroPagos = 1
    elif formaPago == "2":
        if fechaInicio.year == fechaFin.year:
            numeroPagos = meses
        else:
            if fechaInicio.month < fechaFin.month:
                numeroPagos = meses
            else:
                numeroPagos = meses
        
    elif formaPago == "3":
        if fechaInicio.year == fechaFin.year:
            numeroPagos = ceil(abs(fechaFin.month - fechaInicio.month) / 3)
        else:
            if fechaInicio.month < fechaFin.month:
                numeroPagos = ceil(abs(fechaInicio.year - fechaFin.year) * 4 + abs(fechaInicio.month - fechaFin.month) / 3)
            else:
                numeroPagos = ceil(abs(fechaInicio.year - fechaFin.year) * 4 - abs(fechaInicio.month - fechaFin.month) / 3)
    elif formaPago == "4":
        if fechaInicio.year == fechaFin.year:
            numeroPagos = 1
        else:
            numeroPagos = abs(fechaFin.year - fechaInicio.year) + 1

    importePlazo = importe * meses / numeroPagos
    
    for pos in range(numeroPagos):
        item = pos + 1
        if item == 1:
            fecha = fechaInicio + timedelta(days=-1)
        else:
            if formaPago == "2":
                fecha = fechaInicio + timedelta(days=30*pos)
            elif formaPago == "3":
                fecha = fechaInicio + timedelta(days=30*3*pos)
            elif formaPago == "4":
                fecha = fechaInicio + timedelta(years=item-1)
        
        tempPago = clasePagos.objects.create(
            reservaId = numReserva,
            pagoFecha = fecha,
            pagoImporte = importePlazo,
            pagoForma = formaPago,
            pagoPlazoTotal = numeroPagos,
            pagoPlazoActual = item
            )
    
    return None