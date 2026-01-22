from flask import Flask, request, jsonify
from supabase import create_client

# =========================
# APP
# =========================
app = Flask(__name__)

# =========================
# SUPABASE
# =========================
SUPABASE_URL = "https://wkbltctqqsuxqhlbnoeg.supabase.co"
SUPABASE_KEY = "sb_publishable_vpm9GsG9AbVjH80qxfzIfQ_RuFq8uAd"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# =========================
# HOME
# =========================
@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Directorio UMAYOR</title>

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
    border-radius: 14px;
    box-shadow: 0 0 20px rgba(0,0,0,0.1);
}

.header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 20px;
}

.header img {
    height: 50px;
}

input, select, button {
    width: 100%;
    padding: 12px;
    margin: 8px 0;
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

/* Tabla responsiva */
.table-wrapper {
    overflow-x: auto;
    margin-top: 20px;
}

table {
    width: 100%;
    border-collapse: collapse;
    min-width: 1000px;
}

th, td {
    border: 1px solid #ddd;
    padding: 8px;
    vertical-align: top;
}

th {
    background: #005baa;
    color: white;
    text-align: left;
}

.restriccion-ok {
    color: green;
    font-weight: bold;
}

.restriccion-warning {
    color: orange;
    font-weight: bold;
}

.restriccion-dot {
    color: green;
    font-size: 18px;
}

.restriccion-dot-orange {
    color: orange;
    font-size: 18px;
}
</style>
</head>

<body>
<div class="card">

<div class="header">
    <img src="https://raw.githubusercontent.com/EduFerradamonitor/directorio-umayor/main/logoum.jpg">
    <h1>Directorio UMAYOR</h1>
</div>

<input id="busqueda" placeholder="¿Qué escuela busca? (ej: agr, vet, derecho)">
<select id="sede">
    <option value="">Todas las sedes</option>
    <option value="santiago">Santiago</option>
    <option value="temuco">Temuco</option>
</select>

<button onclick="buscar()">Buscar</button>
<button class="secondary" onclick="borrar()">Borrar</button>

<div class="table-wrapper" id="resultados"></div>

</div>

<script>
function iconoRestriccion(valor) {
    if (!valor) return "<span class='restriccion-dot-orange'>● Sin info</span>";

    valor = valor.toLowerCase();

    if (valor.includes("solo correo")) {
        return "<span class='restriccion-dot'>● Solo correo secretaría</span>";
    }
    if (valor.includes("validacion")) {
        return "⚠️ <span class='restriccion-warning'>Validación previa</span>";
    }
    if (valor.includes("autorizacion")) {
        return "🔒 Autorización expresa";
    }
    return valor;
}

function buscar() {
    const q = document.getElementById("busqueda").value;
    const sede = document.getElementById("sede").value;

    fetch(`/buscar?q=${encodeURIComponent(q)}&sede=${encodeURIComponent(sede)}`)
    .then(r => r.json())
    .then(data => {
        if (!data || data.length === 0) {
            document.getElementById("resultados").innerHTML = "<p>No se encontraron resultados.</p>";
            return;
        }

        let html = "<table><tr>" +
            "<th>Nombre</th><th>Escuela</th><th>Cargo</th><th>Campus</th>" +
            "<th>Correo Director</th><th>Secretaría</th><th>Correo Secretaría</th>" +
            "<th>Sede</th><th>Restricción</th></tr>";

        data.forEach(r => {
            html += `<tr>
                <td>${r.nombre || ""}</td>
                <td>${r.escuela_busqueda || r.escuela || ""}</td>
                <td>${r.cargo || ""}</td>
                <td>${r.campus || ""}</td>
                <td>${r.correo_director || ""}</td>
                <td>${r.secretaria || ""}</td>
                <td>${r.correo_secretaria || ""}</td>
                <td>${r.sede || ""}</td>
                <td>${iconoRestriccion(r.consultar_antes_de_entregar_contactos)}</td>
            </tr>`;
        });

        html += "</table>";
        document.getElementById("resultados").innerHTML = html;
    });
}

function borrar() {
    document.getElementById("busqueda").value = "";
    document.getElementById("sede").value = "";
    document.getElementById("resultados").innerHTML = "";
}
</script>
</body>
</html>
"""

# =========================
# BUSCAR
# =========================
@app.route("/buscar")
def buscar():
    q = request.args.get("q", "").strip().lower()
    sede = request.args.get("sede", "").strip().lower()

    if len(q) < 2:
        return jsonify([])

    query = (
        supabase
        .table("directorio_escuelas_umayor")
        .select("*")
        .or_(
            f"escuela_busqueda.ilike.%{q}%,"
            f"escuela.ilike.%{q}%,"
            f"nombre.ilike.%{q}%,"
            f"cargo.ilike.%{q}%"
        )
    )

    if sede:
        query = query.eq("sede", sede)

    result = query.execute()
    return jsonify(result.data or [])

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)






