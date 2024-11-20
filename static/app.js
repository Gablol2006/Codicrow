document.getElementById("run-code").addEventListener("click", function() {
    const code = document.getElementById("code-editor").value;
    const language = document.getElementById("language").value;

    // Enviar el código y el lenguaje al servidor mediante fetch
    fetch("/run", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ code: code, language: language })
    })
    .then(response => response.json())
    .then(data => {
        // Mostrar el resultado en el <pre> con id="output"
        document.getElementById("output").textContent = data.output;
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("output").textContent = "Error al ejecutar el código.";
    });
});

