var ctx = document.getElementById('myChart').getContext('2d');


var graphData = {
    type: 'line',
    data: {
        labels: ['', '', '', '', '', '', '', '', '', '', '', ''],
        datasets: [{
            label: 'Temperatura',
            data: [ , , , , , , , , , , , ],
            backgroundColor: [
                'rgba(73, 198, 230, 0.5)',
            ],
           
            borderWidth: 1
        }]
    },
    options: { }
}

var myChart = new Chart(ctx, graphData);




var socket = new WebSocket('ws://localhost:8000/ws/Sensores/')

socket.onmessage = function(e){
    var djangoData = JSON.parse(e.data);
    console.log(djangoData);

    //var newGraphData = graphData.data.datasets[0].data;
    //newGraphData = djangoData.value;
    //newGraphData.shift(); // Elimina primera posicion del array ( valor mas antiguo de temperatura)
    //newGraphData.push(djangoData.value); //Añado el valor ¿en ultima posicion?
    graphData.data.datasets[0].data = djangoData.value;
    //myChart.update();

    //var newGraphLabel = graphData.data.labels;
    //newGraphLabel.shift();
    //newGraphLabel.push(djangoData.hora);
    graphData.data.labels = djangoData.hora;
    //graphData.data.labels = newGraphLabel;
    myChart.update();

    if(djangoData.bombilla == 0)
    {
        imagenBombilla.src = 'static/bombillaapagada.png';
        document.getElementById('TextoEntrada').innerHTML='Luz apagada';
    } else if (djangoData.bombilla == 1)
    {
        imagenBombilla.src = 'static/bombillaencendida.png';
        document.getElementById('TextoEntrada').innerHTML='Presencia detectada. Luz encendida';

    }
    else {
        imagenBombilla.src = 'static/bombillaapagada.png';
        document.getElementById('TextoEntrada').innerHTML='Luz apagada';
    }
    /*print("djangoData.bombilla");*/

    if(djangoData.estadoToldo == "0"){
        document.getElementById("switch-label2").checked = 0;
    } else if (djangoData.estadoToldo == "1"){
        document.getElementById("switch-label2").checked = 1;
    }



    document.getElementById('textoTemperatura').innerHTML= String(djangoData.temperatura) + " ºC";
    document.getElementById('textoHumedad').innerHTML= String(djangoData.humedad) + " %";
    //document.getElementById('textoCo2').innerHTML= String(djangoData.co2) + " ppm";
    document.getElementById('textoLluvia').innerHTML= "Lluvia a las " + String(djangoData.horaLluvia) + ": " + String(djangoData.lluvia) + " %";
    document.getElementById('textoViento').innerHTML= "Velocidad viento a las " + String(djangoData.horaLluvia) + ": " + + String(djangoData.velocidadViento) + " m/s";
    document.getElementById('textoRafaga').innerHTML= "Rafaga viento a las " + String(djangoData.horaLluvia) + ": " + String(djangoData.rafagaViento) + " m/s";
   
    
    

    console.log(imagenBombilla);
    imagenBombilla.update();

}