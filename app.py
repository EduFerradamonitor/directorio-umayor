from flask import Flask, request, jsonify
from supabase import create_client

app = Flask(__name__)

SUPABASE_URL = "https://wkbltctqqsuxqhlbnoeg.supabase.co"
SUPABASE_KEY = "sb_publishable_vpm9GsG9AbVjH80qxfzIfQ_RuFq8uAd"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Directorio UMAYOR</title>

<!-- Font Awesome -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

<style>
body {
    font-family: Calibri, Arial, sans-serif;
    background: #f3f6f9;
}

.card {
    max-width: 1200px;
    margin: 40px auto;
    background: white;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 0 20px rgba(0,0,0,0.1);
}

.header {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 25px;
}

.header img {
    height: 70px;
}

input, select, button {
    width: 100%;
    padding: 12px;
    margin: 10px 0;
    font-size: 16px;
}

button {
    background: #005baa;
    color: white;
    border: none;
    cursor: pointer;
}

button.secondary {
    background: #999;
}

.table-container {
    overflow-x: auto;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

th, td {
    border: 1px solid #ddd;
    padding: 8px;
    vertical-align: top;
}

th {
    background: #005baa;
    color: white;
}

.restriccion-validacion {
    color: #ff8c00;
    font-weight: bold;
}

.restriccion-secretaria {
    color: green;
    font-weight: bold;
}

.restriccion-vacia {
    color: #999;
}

.footer {
    margin-top: 40px;
    padding-top: 15px;
    border-top: 1px solid #ddd;
    text-align: center;
    font-size: 13px;
    color: #666;
}
</style>
</head>

<body>
<div class="card">

    <div class="header">
        <img src="/static/logoum.jpg">
        <h1>Directorio UMAYOR</h1>
    </div>

    <input id="busqueda" placeholder="¿Qué escuela busca?">
    
    <select id="sede">
        <option value="">Todas las sedes</option>
        <option value="santiago">Santiago</option>
        <option value="temuco">Temuco</option>
    </select>

    <button onclick="buscar()">Buscar</button>
    <button class="secondary" onclick="borrar()">Borrar</button>

    <div id="resultados"></div>

    <div class="footer">
        Desarrollado por <strong>Eduardo Ferrada</strong><br>
        Universidad Mayor · Enero 2026<br>
        Flask · Supabase · Render · Font Awesome
    </div>
</div>

<script>
function buscar() {
    const q = busqueda.value;
    const sede = document.getElementById("sede").value;

    fetch(`/buscar?q=${encodeURIComponent(q)}&sede=${encodeURIComponent(sede)}`)
    .then(r => r.json())
    .then(data => {
        if (!data.length) {
            resultados.innerHTML = "<p>No se encontraron resultados.</p>";
            return;
        }

        let html = `<div class="table-container"><table><tr>
            <th>Nombre</th><th>Escuela</th><th>Cargo</th><th>Campus</th>
            <th>Correo Director</th><th>Secretaría</th><th>Correo Secretaría</th>
            <th>Sede</th><th>Restricción</th></tr>`;

        data.forEach(r => {
            let icono = '<i class="fa-solid fa-circle-minus"></i> Sin restricción';
            let clase = "restriccion-vacia";

            if (r.consultar_antes_de_entregar_contactos?.includes("validacion")) {
                icono = '<i class="fa-solid fa-triangle-exclamation"></i> Validación previa';
                clase = "restriccion-validacion";
            } else if (r.consultar_antes_de_entregar_contactos?.includes("secretaria")) {
                icono = '<i class="fa-solid fa-circle-check"></i> Solo correo secretaría';
                clase = "restriccion-secretaria";
            }

            html += `<tr>
                <td>${r.nombre||""}</td>
                <td>${r.escuela_busqueda||""}</td>
                <td>${r.cargo||""}</td>
                <td>${r.campus||""}</td>
                <td>${r.correo_director||""}</td>
                <td>${r.secretaria||""}</td>
                <td>${r.correo_secretaria||""}</td>
                <td>${r.sede||""}</td>
                <td class="${clase}">${icono}</td>
            </tr>`;
        });

        html += "</table></div>";
        resultados.innerHTML = html;
    });
}

function borrar() {
    busqueda.value = "";
    sede.value = "";
    resultados.innerHTML = "";
}

document.addEventListener("keydown", e => {
    if (e.key === "Enter") buscar();
});
</script>

</body>
</html>
"""

@app.route("/buscar")
def buscar():
    q = request.args.get("q","").lower()
    sede = request.args.get("sede","").lower()

    if len(q) < 2:
        return jsonify([])

    query = supabase.table("directorio_escuelas_umayor").select("*").or_(
        f"nombre.ilike.%{q}%,escuela.ilike.%{q}%,escuela_busqueda.ilike.%{q}%,cargo.ilike.%{q}%"
    )

    if sede:
        query = query.eq("sede", sede)

    return jsonify(query.execute().data or [])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)







