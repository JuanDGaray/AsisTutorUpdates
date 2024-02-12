const Data = [];


function CreateBarInit() {
    const Modules = Data[12]
    const TotalAct = [Data[4],Data[3],Data[5]]; //Enviadas, no_revisadas, no_enviadas
    const TotalAttend = Data[3];
    const TotalMiss = Data[5];
    const TotalActNoAttend = Data[11];
    const TotalAssiAttend = Data[10];
    const TotalClassNoAttend = Data[11] - Data[10];
    const NAssiAttend = Data[13];
    const NClassNoAttend = Data[14] - Data[13];
    const LessonAttend = Data[16];
    const LessonTotal = Data[17];
    CreateBarScore(LessonTotal, LessonAttend, Modules);
    CreateAtendScore(TotalAssiAttend, TotalClassNoAttend, NAssiAttend, NClassNoAttend, Modules);
    CreateBarTaskSend(TotalAct, TotalAttend, TotalMiss, TotalActNoAttend);
    DataBasic()

  }
  

function CreateBarTaskSend(DataAct, ActAttend,ActMiss, ActNoAttend){
  var ctx = document.getElementById('taskSends').getContext('2d');
var myChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ['Entregadas ['+DataAct[0]+']', 'Sin Entregar ['+DataAct[2]+']', 'Por Calificar['+DataAct[1]+']'],
    datasets: [{
      data: [[DataAct[0]],DataAct[2], DataAct[1]],
      backgroundColor: [
        '#92fd70',
        '#FF6384',
        '#FFCE56'
      ],
      borderWidth: 0
    }]
  },
  options: {
    responsive: true,
    cutout: '70%',
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
            usePointStyle: true, // Habilita el uso de estilos de puntos
            pointStyle: 'rect', // Cambia el estilo de punto a un rectángulo
            fontSize: 16
        }
      },
      datalabels: {
        formatter: function(value, context) {
            return value + ' (' + context.dataset.data[context.dataIndex] + '%)';
        },
        color: '#fff',
        font: {
            weight: 'bold'
        }
    }
    }
  }
});

}

function CreateAtendScore(asistenciaReal, totalClases, NAttend, NMiss, modCheck, ){
  const ctx = document.getElementById('Asistence').getContext('2d');
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: modCheck,
        datasets: [
            {
                label: 'Asitió['+NAttend+']',
                data: asistenciaReal,
                borderColor: '#a2d4f5',
                fill: true,
                backgroundColor: '#8BC6EC ',
            },
            {
                label: 'Faltó ['+NMiss+']',
                data: totalClases,
                borderColor: '#48c721',
                backgroundColor: '#48c721a4',
                fill: true
            }
        ]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true,
                max: 5 // Ajusta el valor máximo del eje Y según tus necesidades
            }
        },
        

    }
});
}
function CreateBarScore(ListLessonTotal, ListLessonAttend, modCheck){
  const linearCharts = document.getElementById('scatter-chart').getContext('2d');
  // Crea un nuevo gráfico de barras apiladas
  var grafico = new Chart(linearCharts, {
    type: 'bar',
    data: {
      labels: modCheck, // Ejemplo de etiquetas
      datasets: [{
        label: 'Actividades Totales',
        data: ListLessonTotal, // Datos para la barra 1
        backgroundColor: 'rgba(0, 123, 255, 0.2)', // Color de fondo para la barra 1
        borderColor: 'rgba(0, 123, 255, 1)', // Color del borde para la barra 1
        borderWidth: 1
      }, {
        label: 'Actividades cumplidas',
        data: ListLessonAttend, // Datos para la barra 2
        backgroundColor: 'rgba(255, 99, 132, 0.2)', // Color de fondo para la barra 2
        borderColor: 'rgba(255, 99, 132, 1)', // Color del borde para la barra 2
        borderWidth: 1
      }]
    },
options: {
      scales: {
        x: {
          stacked: true // Apilar las barras horizontalmente
        },
        y: {
          beginAtZero: true,
          stacked: false
        }
      },
      plugins: {
        datalabels: [ChartDataLabels]
      }
    }
  });
}

function DataBasic(){
  document.getElementById("%ActivitiesClass").innerHTML = Data[7]+'%';
  document.getElementById("%ActivitiesHome").innerHTML = Data[6]+'%';
  document.getElementById("%AsisClass").innerHTML = Data[15]+'%';

}
CreateBarInit()
