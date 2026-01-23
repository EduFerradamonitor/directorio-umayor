from flask import Flask, request, jsonify, url_for
from supabase import create_client

app = Flask(__name__)

# =========================
# CONFIGURACIÓN SUPABASE
# =========================
SUPABASE_URL = "https://wkbltctqqsuxqhlbnoeg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndrYmx0Y3RxcXN1eHFobGJub2VnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjkwMDI1NzYsImV4cCI6MjA4NDU3ODU3Nn0.QLl8XI79jOC_31RjtTMCwrKAXNg-Y1Bt_x2JQL9rnEM"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# =========================
# PÁGINA PRINCIPAL
# =========================
@app.route("/")
def home():
    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Directorio Escuelas UM</title>

<style>
body {{
    font-family: Calibri, Arial, sans-serif;
    background: #f3f6f9;
}}

.card {{
    max-width: 1200px;
    margin: 40px auto;
    background: white;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 0 20px rgba(0,0,0,0.1);
}}

.header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.logo-um {{
    height: 80px;
}}

.info-box {{
    margin: 20px 0;
    padding: 14px 16px;
    background: #f0f6ff;
    border-left: 4px solid #005baa;
    font-size: 16px;
    font-weight: bold;
}}

input, select, button {{
    width: 100%;
    padding: 12px;
    margin: 10px 0;
    font-size: 16px;
}}

button {{
    background: #005baa;
    color: white;
    border: none;
    cursor: pointer;
}}

button.secondary {{
    background: #999;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}}

th, td {{
    border: 1px solid #ddd;
    padding: 10px;
    vertical-align: top;
}}

th {{
    background: #005baa;
    color: white;
}}

.tooltip {{
    position: relative;
    display: inline-block;
    cursor: pointer;
    margin-left: 6px;
}}

.tooltip .tooltip-box {{
    visibility: hidden;
    width: 260px;
    background-color: #333;
    color: #fff;
    text-align: left;
    border-radius: 6px;
    padding: 10px;
    position: absolute;
    z-index: 10;
    top: 22px;
    left: 0;
}}

.tooltip:hover .tooltip-box {{
    visibility: visible;
}}

.tooltip a {{
    color: #aad4ff;
    text-decoration: underline;
}}

.footer {{
    margin-top: 30px;
    font-size: 13px;
    color: #555;
    text-align: center;
}}
</style>
</head>

<body>
<div class="card">

    <div class="header">
        <h1>Directorio Escuelas UM</h1>
        <img src="{url_for('static', filename='img/logoum.jpg')}" class="logo-um">
    </div>

    <div class="info-box">
        ℹ️ Al primer ingreso del día, la carga puede demorar unos segundos.  
        Si no ves el buscador de inmediato, espera o actualiza la página.  
        Para ver más información de directores y secretarías, haz clic en el ícono ℹ️ junto al nombre.
    </div>

    <input id="busqueda" placeholder="¿Qué escuela busca?" onkeydown="if(event.key==='Enter') buscar();">

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
        Universidad Mayor · Enero 2026
    </div>

</div>

<script>
function buscar() {{
    const q = document.getElementById("busqueda").value;
    const sede = document.getElementById("sede").value;

    if (q.length < 3) {{
        document.getElementById("resultados").innerHTML =
            "<p>Ingresa al menos 3 caracteres para buscar.</p>";
        return;
    }}

    fetch(`/buscar?q=${{encodeURIComponent(q)}}&sede=${{encodeURIComponent(sede)}}`)
    .then(r => r.json())
    .then(data => {{
        if (!data || data.length === 0) {{
            document.getElementById("resultados").innerHTML =
                "<p>No se encontraron resultados.</p>";
            return;
        }}

        let html = `<table>
        <tr>
            <th>Director</th>
            <th>Escuela</th>
            <th>Cargo</th>
            <th>Campus</th>
            <th>Secretaría</th>
            <th>Sede</th>
        </tr>`;

        data.forEach(r => {{
            html += `<tr>
                <td>
                    ${r.nombre || ""}
                    <span class="tooltip">ℹ️
                        <div class="tooltip-box">
                            <strong>Correo:</strong>
                            <a href="mailto:${r.correo_director || ""}">
                                ${r.correo_director || "Sin información"}
                            </a><br>
                            <strong>Anexo:</strong> ${r.anexo_director || "Sin información"}<br>
                            <strong>Restricción:</strong> ${r.consultar_antes_de_entregar_contactos || "Sin restricción"}
                        </div>
                    </span>
                </td>
                <td>${r.escuela_busqueda || r.escuela || ""}</td>
                <td>${r.cargo || ""}</td>
                <td>${r.campus || ""}</td>
                <td>
                    ${r.secretaria || "No informado"}
                    <span class="tooltip">ℹ️
                        <div class="tooltip-box">
                            <strong>Correo:</strong>
                            <a href="mailto:${r.correo_secretaria || ""}">
                                ${r.correo_secretaria || "Sin información"}
                            </a><br>
                            <strong>Anexo:</strong> ${r.anexo_secretaria || "Sin información"}
                        </div>
                    </span>
                </td>
                <td>${r.sede || ""}</td>
            </tr>`;
        }});

        html += "</table>";
        document.getElementById("resultados").innerHTML = html;
    });
}}

function borrar() {{
    document.getElementById("busqueda").value = "";
    document.getElementById("sede").value = "";
    document.getElementById("resultados").innerHTML = "";
}}
</script>

</body>
</html>
"""

# =========================
# BUSCADOR API
# =========================
@app.route("/buscar")
def buscar_api():
    q = request.args.get("q", "").strip()
    sede = request.args.get("sede", "").strip()

    if len(q) < 3:
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
        query = query.ilike("sede", sede)

    result = query.execute()
    return jsonify(result.data if result.data else [])

# =========================
# EJECUCIÓN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
