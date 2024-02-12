const Data1 = [];
var StdName = Data1[1];
const StdAge = Data1[19];
var StdPhone = Data1[18];
const StGender = 'Male';
const UrlImgProfile = null
const StatusProfileImg = false;
if (Data1.length >0){ 
    if (StdPhone.startsWith("+")) {
        StdPhone = StdPhone.substring(1);
    }}

function procesarNumero(numero) {
    let score;
    if (numero >= 0 && numero <= 20) {
        score = '0 - 20'
    } else if (numero > 20 && numero <= 40) {
        score = '20 - 40'
    } 
    else if (numero > 40 && numero <= 60) {
        score = '40 - 60'
    }
    else if (numero > 60 && numero <= 80) {
        score = '60 - 80'
    }
    else if (numero > 80 && numero <= 90) {
        score = '80 - 90'
    }
    else if (numero > 90 && numero <= 100) {
        score = '90 - 100'
    }
    return score

}

window.onload = function() {

        let Attend = procesarNumero(Data1[15]);
        let tasksHome = procesarNumero(Data1[6]);
        let tasksClass = procesarNumero(Data1[7]);
        console.log(Attend, tasksHome, tasksClass )
        let score1 = '80 - 90'


        const inputsMetrics = {
        'attend': {
                '0 - 20': StdName+'%20presenta%20una%20asitencia%20algo%20baja.%20Aunque%20sabemos%20que%20cada%20día%20trae%20consigo%20desafíos,%20queremos%20animar%20a%20'+StdName+'%20a%20que%20se%20una%20a%20nosotros%20con%20más%20frecuencia.%20¡Cada%20clase%20es%20una%20oportunidad%20única%20de%20aprender%20y%20crecer!',
                '20 - 40': ''+StdName+'%20ha%20mostrado%20un%20progreso%20en%20la%20asistencia,%20¡y%20eso%20es%20asombroso!%20Sin%20embargo,%20aún%20hay%20espacio%20para%20mejorar%20la%20 consistencia%20en%20la%20participación%20en%20clase.%20¡Estamos%20emocionados%20de%20verte%20más%20a%20menudo%20en%20nuestras%20lecciones!',
                '40 - 60': 'La%20asistencia%20de%20'+StdName+'%20es%20moderada,%20pero%20imaginamos%20que%20con%20un%20poco%20más%20de%20regularidad,%20el%20aprendizaje%20será%20aún%20más%20constante.%20¡Cada%20clase%20cuenta%20una%20historia%20de%20descubrimiento%20y%20oportunidades,%20y%20estamos%20ansiosos%20por%20compartir%20más%20de%20ellas%20contigo!',
                '60 - 80': ''+StdName+'%20ha%20demostrado%20una%20buena%20asistencia,%20y%20eso%20está%20teniendo%20un%20impacto%20positivo%20en%20su%20desarrollo%20académico.%20¡Cada%20día%20en%20clase%20es%20un%20paso%20más%20hacia%20el%20éxito,%20y%20estamos%20encantados%20de%20que%20estés%20aprovechando%20estas%20oportunidades!',
                '80 - 90': ''+StdName+'%20ha%20mantenido%20una%20asistencia%20sólida,%20lo%20cual%20es%20fundamental%20para%20el%20éxito%20académico.%20¡Bravo!%20Cada%20clase%20a%20la%20que%20asistes%20es%20una%20inversión%20valiosa%20en%20tu%20futuro,%20y%20estamos%20emocionados%20de%20ser%20parte%20de%20tu%20viaje%20educativo.',
                '90 - 100': 'La%20asistencia%20de%20'+StdName+'%20estudiante%20es%20excepcional.%20¡Su%20compromiso%20constante%20es%20digno%20de%20elogio%20y%20refleja%20una%20actitud%20seria%20hacia%20el%20aprendizaje!%20Cada%20clase%20contigo%20es%20un%20recordatorio%20de%20cómo%20el%20esfuerzo%20y%20la%20dedicación%20dan%20sus%20frutos.%20¡Estamos%20emocionados%20de%20seguir%20creciendo%20y%20aprendiendo%20juntos!'
                },

        'scoreHome': {
                '0 - 20': ''+StdName+',%20en%20cuanto%20a%20las%20tareas%20en%20casa,%20sabemos%20que%20cada%20esfuerzo%20cuenta.%20Tu%20dedicación%20ya%20es%20admirable,%20y%20te%20animamos%20a%20dedicar%20un%20poco%20más%20de%20tiempo.%20Cada%20paso%20adicional%20que%20tomes%20marcará%20una%20gran%20diferencia%20en%20tu%20viaje%20de%20aprendizaje.%20¡Estamos%20aquí%20para%20apoyarte%20en%20cada%20paso!',
                '20 - 40': ''+StdName+',%20tus%20esfuerzos%20en%20las%20tareas%20en%20casa%20son%20notables.%20Cada%20paso%20que%20tomas%20muestra%20tu%20compromiso.%20Aún%20hay%20espacio%20para%20crecer%20y%20alcanzar%20niveles%20aún%20más%20sólidos.%20Estamos%20aquí%20para%20apoyarte%20en%20cada%20desafío%20y%20celebrar%20cada%20logro.%20¡Sigue%20brillando!',
                '40 - 60': ''+StdName+',%20en%20tus%20tareas%20en%20casa,%20estás%20demostrando%20un%20compromiso%20valioso.%20Cada%20tarea%20es%20una%20oportunidad%20emocionante%20para%20aprender%20y%20crecer.%20Tu%20dedicación%20contribuirá%20enormemente%20a%20tu%20progreso%20académico.%20¡Sigue%20así,%20cada%20esfuerzo%20cuenta!',
                '60 - 80': ''+StdName+',%20queremos%20destacar%20tu%20consistencia%20y%20esfuerzo%20constante%20en%20las%20tareas%20en%20casa.%20Cada%20tarea%20completada%20es%20un%20paso%20hacia%20adelante%20en%20tu%20aprendizaje%20independiente.%20Tu%20dedicación%20no%20pasa%20desapercibida,%20¡y%20estamos%20emocionados%20por%20lo%20que%20lograrás%20a%20continuación!',
                '80 - 90': '¡Increíble,%20'+StdName+'!%20Tus%20logros%20en%20las%20tareas%20en%20casa%20son%20notables.%20Mantener%20una%20entrega%20y%20calidad%20tan%20consistentes%20es%20digno%20de%20elogio.%20Tu%20compromiso%20y%20dedicación%20son%20realmente%20impresionantes.%20Sigue%20brillando%20y%20desafiándote%20a%20ti%20mismo,%20¡estamos%20emocionados%20de%20ser%20parte%20de%20tu%20viaje!',
                '90 - 100': ''+StdName+',%20has%20alcanzado%20un%20nivel%20excepcional%20en%20tus%20tareas%20en%20casa.%20Tu%20dedicación%20y%20excelencia%20son%20una%20inspiración%20para%20todos.%20Cada%20tarea%20que%20completas%20es%20un%20testimonio%20de%20tu%20arduo%20trabajo%20y%20determinación.%20¡Estamos%20emocionados%20por%20ver%20hacia%20dónde%20te%20llevará%20tu%20increíble%20dedicación!'
                },

        'scoreClass': {
                '0 - 20': 'La%20participación%20y%20comprensión%20en%20clase%20de%20'+StdName+'%20son%20limitadas.%20Se%20sugiere%20una%20mayor%20interacción%20para%20fortalecer%20la%20asimilación%20de%20conceptos.%20Cada%20oportunidad%20en%20clase%20es%20una%20posibilidad%20de%20crecimiento.%20¡Anímate%20a%20participar%20más!',
                '20 - 40': 'El%20estudiante%20'+StdName+'%20ha%20mostrado%20cierta%20participación%20en%20clase,%20pero%20se%20anima%20a%20involucrarse%20más%20para%20aprovechar%20al%20máximo%20las%20lecciones.%20Tu%20participación%20hace%20que%20la%20clase%20sea%20más%20rica%20y%20diversa.%20¡Sigue%20adelante!',
                '40 - 60': 'La%20participación%20en%20clase%20de%20'+StdName+'%20es%20moderada.%20Continuar%20contribuyendo%20en%20las%20discusiones%20será%20beneficioso%20para%20un%20mejor%20entendimiento.%20Cada%20interacción%20suma%20valor%20a%20la%20experiencia%20educativa.%20¡Sigamos%20construyendo%20juntos!',
                '60 - 80': 'Este%20estudiante,%20'+StdName+',%20ha%20mantenido%20un%20buen%20desempeño%20en%20clase,%20participando%20de%20manera%20activa%20y%20demostrando%20una%20comprensión%20sólida.%20Tu%20dedicación%20es%20inspiradora,%20y%20tu%20contribución%20enriquece%20nuestra%20experiencia%20de%20aprendizaje.',
                '80 - 90': 'La%20participación%20en%20clase%20de%20'+StdName+'%20es%20muy%20buena.%20El%20estudiante%20muestra%20un%20compromiso%20destacado%20en%20las%20lecciones%20y%20contribuye%20positivamente%20al%20entorno%20de%20aprendizaje.%20Cada%20vez%20que%20participas,%20inspiras%20a%20otros%20a%20hacer%20lo%20mismo.%20¡Sigue%20brillando!',
                '90 - 100': 'La%20participación%20y%20desempeño%20en%20clase%20de%20'+StdName+'%20son%20excepcionales.%20Este%20estudiante%20demuestra%20una%20comprensión%20profunda%20y%20un%20compromiso%20sobresaliente.%20Tu%20dedicación%20es%20un%20ejemplo%20para%20todos,%20y%20tu%20entusiasmo%20hace%20que%20la%20clase%20sea%20más%20enriquecedora.'
                }
        }

        var text = 'Hola%20'+StdName+'%20%F0%9F%98%8A%0A%0A*Quiero%20comentarte%20sobre%20tu%20rendimiento%20en%20clase*%0A%0A*Tareas%20entregadas:*%20'+(Data[3] + Data[4])+'%20|%20*Tareas%20Sin%20entregar:*%20'+Data1[5]+'%0A%0A*Tu asistencia:*%0A*'+inputsMetrics["attend"][Attend]+'%0A%0A*Tus Tareas entregadas:*%0A'+inputsMetrics['scoreHome'][tasksHome]+'%0A'+inputsMetrics['scoreClass'][tasksClass]+'%0A%0A*Tu Puntaje:*%0A%0A'+inputsMetrics['scoreClass'][score1];
    
    var imgElement = document.getElementById('ImgProfile');
    document.getElementById('NameStudent').innerHTML = StdName;
    document.getElementById('Agetudent').innerHTML = StdAge;
    document.getElementById('linkWA').href = "https://api.whatsapp.com/send/?phone="+StdPhone+"&text="+text+"&type=phone_number&app_absent=0"
    if (StatusProfileImg == true) {
        imgElement.style.backgroundImage  = UrlImgProfile
    }
};



function captureScreen() {
    html2canvas(document.getElementById('main')).then(function(canvas) {
        var link = document.createElement('a');
        link.href = canvas.toDataURL();
        link.download = StdName +'.png';
        link.click();
    });
}