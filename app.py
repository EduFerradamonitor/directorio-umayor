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
# HOME
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
    height: 90px;
    object-fit: contain;
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

.table-container {{
    overflow-x: auto;
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
    white-space: nowrap;
}}

.name-cell {{
    display: flex;
    align-items: center;
    gap: 6px;
}}

.info-btn {{
    background: none;
    border: none;
    color: #005baa;
    cursor: pointer;
    font-weight: bold;
}}

.tooltip {{
    display: none;
    position: absolute;
    background: #fff;
    border: 1px solid #ccc;
    padding: 10px;
    border-radius: 6px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    z-index: 1000;
    max-width: 260px;
    font-size: 14px;
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

<input id="busqueda" placeholder="¿Qué escuela busca?" onkeydown="if(event.key==='Enter') buscar();">

<select id="sede">
    <option value="">Todas las sedes</option>
    <option value="santiago">Santiago</option>
    <option value="temuco">Temuco</option>
</select>

<button onclick="buscar()">Buscar</button>
<button class="secondary" onclick="borrar()">Borrar</button>

<div class="table-container">
<div id="resultados"></div>
</div>

<div class="footer">
    Desarrollado por <strong>Eduardo Ferrada</strong><br>
    Universidad Mayor · Enero 2026
</div>

</div>

<div id="tooltip" class="tooltip"></div>

<script>
function showTooltip(event, html) {{
    const t = document.getElementById("tooltip");
    t.innerHTML = html;
    t.style.display = "block";
    t.style.left = event.pageX + 10 + "px";
    t.style.top = event.pageY + 10 + "px";
}}

document.addEventListener("click", e => {{
    if (!e.target.classList.contains("info-btn")) {{
        document.getElementById("tooltip").style.display = "none";
    }}
}});

function buscar() {{
    const q = document.getElementById("busqueda").value;
    const sede = document.getElementById("sede").value;

    fetch(`/buscar?q=${{encodeURIComponent(q)}}&sede=${{encodeURIComponent(sede)}}`)
    .then(r => r.json())
    .then(data => {{
        if (!data || data.length === 0) {{
            document.getElementById("resultados").innerHTML = "<p>No hay resultados.</p>";
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
            const directorInfo = `
                <strong>Correo:</strong> ${{r.correo_director || "No informado"}}<br>
                <strong>Anexo:</strong> ${{r.anexo_director || "Sin información"}}<br>
                <strong>Restricción:</strong> ${{r.consultar_antes_de_entregar_contactos || "Sin restricción"}}
            `;

            const secInfo = `
                <strong>Correo:</strong> ${{r.correo_secretaria || "No informado"}}<br>
                <strong>Anexo:</strong> ${{r.anexo_secretaria || "Sin información"}}
            `;

            html += `<tr>
                <td>
                    <div class="name-cell">
                        ${{r.nombre || ""}}
                        <button class="info-btn" onclick="showTooltip(event, \`${{directorInfo}}\`)">ℹ️</button>
                    </div>
                </td>
                <td>${{r.escuela_busqueda || r.escuela || ""}}</td>
                <td>${{r.cargo || ""}}</td>
                <td>${{r.campus || ""}}</td>
                <td>
                    <div class="name-cell">
                        ${{r.secretaria || "No informado"}}
                        <button class="info-btn" onclick="showTooltip(event, \`${{secInfo}}\`)">ℹ️</button>
                    </div>
                </td>
                <td>${{r.sede || ""}}</td>
            </tr>`;
        }});

        html += "</table>";
        document.getElementById("resultados").innerHTML = html;
    }});
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
# API BUSCAR
# =========================
@app.route("/buscar")
def buscar_api():
    q = request.args.get("q", "").lower()
    sede = request.args.get("sede", "").lower()

    query = supabase.table("directorio_escuelas_umayor").select("*")

    if q:
        query = query.or_(
            f"escuela_busqueda.ilike.%{q}%,escuela.ilike.%{q}%,nombre.ilike.%{q}%,cargo.ilike.%{q}%"
        )

    if sede:
        query = query.ilike("sede", sede)

    res = query.execute()
    return jsonify(res.data or [])

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)




