    function calcular() {
        var numPrecio = document.getElementById("competencia").value * 1.00;
        var modPrecioCompetencia = document.getElementById("competencia").value * 0.9;
        var elementPrecioCompetencia = document.getElementById("precioCompetencia");
        elementPrecioCompetencia.innerHTML = modPrecioCompetencia.toFixed(2) + " €";
        
        var porcTipo = document.getElementById("tipo").value;
        var modTipo =  porcTipo * modPrecioCompetencia;
        var elementModTipo = document.getElementById("difTipo");
        var elementModTipoPorc = document.getElementById("difTipoPorc");
        elementModTipo.innerHTML = modTipo.toFixed(2) + " €"; 
        elementModTipoPorc.innerHTML = (porcTipo * 100) + "%";
        
        var porcUso = document.getElementById("uso").value;
        var modUso =  porcUso * modPrecioCompetencia;
        var elementModUso = document.getElementById("difUso");
        var elementModUsoPorc = document.getElementById("difUsoPorc");
        elementModUso.innerHTML = modUso.toFixed(2) + " €";
        elementModUsoPorc.innerHTML = (porcUso * 100) + "%";
        
        var porcHabitaciones = document.getElementById("habitaciones").value;
        var modHabitaciones =  porcHabitaciones * modPrecioCompetencia;
        var elementModHabitaciones = document.getElementById("difHabitaciones");
        var elementModHabitacionesPorc = document.getElementById("difHabitacionesPorc");
        elementModHabitaciones.innerHTML = modHabitaciones.toFixed(2);
        elementModHabitacionesPorc.innerHTML = (porcHabitaciones * 100) + "%";
        
        var porcBalcon = document.getElementById("balcon").value;
        var modBalcon =  porcBalcon * modPrecioCompetencia;
        var elementModBalcon = document.getElementById("difBalcon");
        var elementModBalconPorc = document.getElementById("difBalconPorc");
        elementModBalcon.innerHTML = modBalcon.toFixed(2) + " €";
        elementModBalconPorc.innerHTML = (porcBalcon * 100) + "%";
        
        var porcAscensor = document.getElementById("ascensor").value;
        var modAscensor =  porcAscensor * modPrecioCompetencia;
        var elementModAscensor = document.getElementById("difAscensor");
        var elementModAscensorPorc = document.getElementById("difAscensorPorc");
        elementModAscensor.innerHTML = modAscensor.toFixed(2) + " €";
        elementModAscensorPorc.innerHTML = (porcAscensor * 100) + "%";
        
        var porcZona = document.getElementById("zona").value;
        var modZona =  porcZona * modPrecioCompetencia;
        var elementModZona = document.getElementById("difZona");
        var elementModZonaPorc = document.getElementById("difZonaPorc");
        elementModZona.innerHTML = modZona.toFixed(2) + " €";
        elementModZonaPorc.innerHTML = (porcZona * 100) + "%";
        
        var porcCama = document.getElementById("cama").value;
        var modCama =  porcCama * modPrecioCompetencia;
        var elementModCama = document.getElementById("difCama");
        var elementModCamaPorc = document.getElementById("difCamaPorc");
        elementModCama.innerHTML = modCama.toFixed(2) + " €";
        elementModCamaPorc.innerHTML = (porcCama * 100) + "%";
        
        var numBanos = document.getElementById("banos").value;
        var numCapacidad = document.getElementById("capacidad").value;
        var propBanos = numBanos / numCapacidad;
        var porcBanos = 0;
        if (propBanos <= 0.2)
            porcBanos = -0.03;
        else if (propBanos <= 0.25)
            porcBanos = 0.01;
        else if (propBanos <= 0.35)
            porcBanos = 0.03;
        else if (propBanos <= 0.45)
            porcBanos = 0.05;
        else if (propBanos <= 0.50)
            porcBanos = 0.07;
        else
            porcBanos = 0.2;
        var modBanos =  porcBanos * modPrecioCompetencia;
        var elementModBanos = document.getElementById("difBanos");
        var elementModBanosPorc = document.getElementById("difBanosPorc");
        elementModBanos.innerHTML = modBanos.toFixed(2) + " €";
        elementModBanosPorc.innerHTML = (porcBanos * 100) + "%";
        
        var numSuperficie = document.getElementById("superficie").value;
        var porcSuperficie = 0;
        if (numSuperficie <= 5)
            porcSuperficie = -0.03;
        else if (numSuperficie <= 7)
            porcSuperficie = 0.01;
        else if (numSuperficie <= 10)
            porcSuperficie = 0.05;
        else if (numSuperficie <= 15)
            porcSuperficie = 0.07;
        else if (numSuperficie <= 20)
            porcSuperficie = 0.1;
        else
            porcSuperficie = 0.12;
        var modSuperficie =  porcSuperficie * modPrecioCompetencia;
        var elementModSuperficie = document.getElementById("difSuperficie");
        var elementModSuperficiePorc = document.getElementById("difSuperficiePorc");
        elementModSuperficie.innerHTML = modSuperficie.toFixed(2) + " €";
        elementModSuperficiePorc.innerHTML = (porcSuperficie * 100).toFixed(0) + "%";
    
        var sumaEstimado = modPrecioCompetencia + modTipo + modUso + modSuperficie + modBanos + modHabitaciones + modBalcon + modAscensor + modZona + modCama;
        var elementSumaEstimado = document.getElementById("precioEstimado");
        elementSumaEstimado.innerHTML = sumaEstimado.toFixed(2) + " €";
        
        var elementCompetencia = document.getElementById("precioCompetencia");
        var numPrecioCompetencia = numPrecio.toFixed(2);
        elementCompetencia.innerHTML = numPrecioCompetencia + " €";
        
        var porcDiferencia = (sumaEstimado / numPrecio - 1) * 100;
        var elementDiferencia = document.getElementById("relacionPrecio");
        var elementDiferenciaPorc = document.getElementById("relacionPrecioPorc");
        elementDiferencia.innerHTML = (sumaEstimado - numPrecio).toFixed(2) + " €";
        elementDiferenciaPorc.innerHTML = porcDiferencia.toFixed(2) + " %";
    }