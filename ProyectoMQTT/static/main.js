var ctx = document.getElementById('myChart').getContext('2d');

var graphData = {
    type: 'line',
    data: {
        labels: ['', '', '', '', '', ''],
        datasets: [{
            label: 'Temperatura',
            data: [ , , , , , ],
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

}