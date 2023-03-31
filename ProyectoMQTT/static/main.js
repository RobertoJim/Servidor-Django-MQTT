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

    document.getElementById('textoTemperatura').innerHTML= String(djangoData.temperatura) + " ºC";
    document.getElementById('textoHumedad').innerHTML= String(djangoData.humedad) + " %";
    document.getElementById('textoCo2').innerHTML= String(djangoData.co2) + " ppm";


}
