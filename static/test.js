let correctas = [2, 3, 1, 1, 3, 3, 1, 2, 1, 3];
let opcion_elegida = [];
let cantidad_correctas= 0;

function respuesta(num_pregunta, seleccionada){
    opcion_elegida[num_pregunta] = seleccionada.value;
    id = "p" + num_pregunta

    labels = document.getElementById(id).childNodes;
    labels[3].style.backgroundColor = "white";
    labels[5].style.backgroundColor = "white";
    labels[7].style.backgroundColor = "white";

    seleccionada.parentNode.style.backgroundColor = "#cec0fc";
}

function corregir(){
    cantidad_correctas = 0;
    for (i=0; i < correctas.length; i++){
        if (correctas[i] == opcion_elegida[i]){
            cantidad_correctas++;
        }
    }
    localStorage.setItem("puntaje", cantidad_correctas);
}

function resul(){
    let resultado = localStorage.getItem("puntaje");
    document.getElementById("resultado").textContent = resultado;
}

function nivelar(){
    let nivel = localStorage.getItem("puntaje");
    let mensaje;

    if (nivel < 5){
        mensaje = "Te recomendamos comenzar en el nivel básico"
    } else if (nivel < 8){
        mensaje = "Te recomendamos comenzar en el nivel intermedio"
    } else{
        mensaje = "Te recomendamos comenzar en el nivel avanzado"
    }
    document.getElementById("mensaj").textContent = mensaje;
}