var ctx = document.getElementById('myChart').getContext('2d');


var graphData = {
    type: 'line',
    data: {
        labels: ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        datasets: [{
            label: 'Temperatura',
            data: [ , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ],
            backgroundColor: [
                'rgba(73, 198, 230, 0.5)',
            ],
           
            borderWidth: 1
        }]
    },
    options: { }
}

var myChart = new Chart(ctx, graphData);

var ip_addr = document.location.hostname; //Obtengo IP del servidor

var argumento = 'ws://' + String(ip_addr) + ':8000/ws/Channels/';

var socket = new WebSocket(argumento);

socket.onmessage = function(e){
    var djangoData = JSON.parse(e.data);
    console.log(djangoData);
    graphData.data.datasets[0].data = djangoData.value;
    graphData.data.labels = djangoData.hora;
    myChart.update();

    if(djangoData.bombilla == 0)
    {
        imagenBombilla.src = 'static/imagenes/bombillaapagada.png';
        document.getElementById('TextoBombilla').innerHTML='Luz apagada';
    } else if (djangoData.bombilla == 1)
    {
        imagenBombilla.src = 'static/imagenes/bombillaencendida.png';
        document.getElementById('TextoBombilla').innerHTML='Presencia detectada. Luz encendida';

    }
    else {
        imagenBombilla.src = 'static/imagenes/bombillaapagada.png';
        document.getElementById('TextoBombilla').innerHTML='Luz apagada';
    }
    /*print("djangoData.bombilla");*/

    if(djangoData.estadoToldo == "0"){
        document.getElementById("switch-label2").checked = 0;
    } else  if (djangoData.estadoToldo == "1"){
        document.getElementById("switch-label2").checked = 1;
        if(djangoData.alertaToldo == 1)
        {
            alert("Se espera lluvia, bajando toldo");
        }
        if(djangoData.mensajeLluvia == 1)
        {
            alert("Ha empezado a llover, bajando toldo");
        }
    }

    if(djangoData.abrirPersiana == "1")
    {
        alert("Hay poca luz y el sol esta fuera, abriendo persiana");
        document.getElementById("letterE").checked = 1;
    }

    if(djangoData.persianaAutomatica == "1")
     {
        document.getElementById("DeshabPersiana").checked = 0;
        
     } else if(djangoData.persianaAutomatica == "0")
     {
        document.getElementById("DeshabPersiana").checked = 1;
     }

    //Para que se actualice el slider en 2 navegadores si estan 2 abiertos a la vez
    if(djangoData.estadoPersiana == "1")
    {
        document.getElementById("letterA").checked = 1;
    } else if (djangoData.estadoPersiana == "2")
    {
        document.getElementById("letterB").checked = 1;
    } else if (djangoData.estadoPersiana == "3")
    {
        document.getElementById("letterC").checked = 1;
    }else if(djangoData.estadoPersiana == "4")
    {
        document.getElementById("letterD").checked = 1;
    }else if(djangoData.estadoPersiana == "5")
    {
        document.getElementById("letterE").checked = 1;
    }



    document.getElementById('textoTemperatura').innerHTML= String(djangoData.temperatura) + " ºC";
    document.getElementById('textoHumedad').innerHTML= String(djangoData.humedad) + " %";
    document.getElementById('textoCo2').innerHTML= String(djangoData.co2) + " ppm";

    document.getElementById('hora').innerHTML = String(djangoData.horaLluvia) + " son:";

    document.getElementById('textoLluvia').innerHTML= "Lluvia: " + String(djangoData.lluvia) + " %";
    document.getElementById('textoViento').innerHTML= "Velocidad viento: " + String(djangoData.velocidadViento) + " m/s";
    document.getElementById('textoRafaga').innerHTML= "Rafaga viento: " + String(djangoData.rafagaViento) + " m/s";
   
    
    

    console.log(imagenBombilla);
    imagenBombilla.update();

}