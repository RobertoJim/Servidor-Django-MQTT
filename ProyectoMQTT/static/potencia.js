var ctx = document.getElementById('myChart').getContext('2d');


var graphData = {
    type: 'line',
    data: {
        labels: ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
        datasets: [{
            label: 'Potencia',
            data: [ , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ],
            backgroundColor: [
                'rgba(73, 198, 230, 0.5)',
            ],
           
            borderWidth: 1
        }]
    },
    options: { }
}

var myChart2 = new Chart(ctx, graphData);

var ip_addr = document.location.hostname; //Obtengo IP del servidor

var argumento = 'ws://' + String(ip_addr) + ':8000/ws/Channels/';

var socket = new WebSocket(argumento);

socket.onmessage = function(e){
    var djangoData = JSON.parse(e.data);
    console.log(djangoData);
    graphData.data.datasets[0].data = djangoData.potencia;
    graphData.data.labels = djangoData.arrayHoraPotencia;
    console.log(djangoData.arrayHoraPotencia)
    myChart2.update();

}
