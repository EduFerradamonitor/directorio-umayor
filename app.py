from flask import Flask, request, jsonify, url_for
from supabase import create_client

app = Flask(__name__)

# =========================
# SUPABASE
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
    max-width: 1100px;
    margin: 30px auto;
    background: white;
    padding: 28px;
    border-radius: 12px;
    box-shadow: 0 0 20px rgba(0,0,0,0.1);
}}

.header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.logo-um {{
    height: 110px;
}}

.filters {{
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 12px;
    margin-top: 20px;
}}

input, select, button {{
    padding: 11px;
    font-size: 15px;
    width: 100%;
}}

button {{
    margin-top: 10px;
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
    table-layout: fixed;
}}

th, td {{
    border: 1px solid #ddd;
    padding: 8px;
    font-size: 14px;
    vertical-align: top;
    word-wrap: break-word;
}}

th {{
    background: #005baa;
    color: white;
}}

.person {{
    color: #005baa;
    text-decoration: underline;
    cursor: pointer;
}}

.tooltip {{
    position: absolute;
    display: none;
    background: #fff;
    border: 1px solid #ccc;
    padding: 10px;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,.2);
    font-size: 13px;
    width: 260px;
    z-index: 9999;
}}

.footer {{
    text-align: center;
    margin-top: 25px;
    font-size: 13px;
    color: #555;
}}
</style>
</head>

<body>
<div class="card">

<div class="header">
<h1>Directorio Escuelas UM</h1>
<img src="{url_for('static', filename='img/logoum.jpg')}" class="logo-um">
</div>

<div class="filters">
<input id="busqueda" placeholder="Buscar escuela, cargo o persona"
       onkeydown="if(event.key==='Enter') buscar();">
<select id="sede">
<option value="">Todas las sedes</option>
<option value="santiago">Santiago</option>
<option value="temuco">Temuco</option>
</select>
</div>

<button onclick="buscar()">Buscar</button>
<button class="secondary" onclick="borrar()">Borrar</button>

<div id="resultados"></div>

<div class="footer">
Desarrollado por <strong>Eduardo Ferrada</strong><br>
Universidad Mayor · Enero 2026
</div>

</div>

<div id="tooltip" class="tooltip"></div>

<script>
const tooltip = document.getElementById("tooltip");

function showTooltip(event, html) {{
    tooltip.innerHTML = html;
    tooltip.style.display = "block";
    tooltip.style.top = (event.pageY + 10) + "px";
    tooltip.style.left = (event.pageX + 10) + "px";
}}

document.addEventListener("click", () => {{
    tooltip.style.display = "none";
}});

function buscar() {{
    const q = document.getElementById("busqueda").value;
    const sede = document.getElementById("sede").value;

    fetch(`/buscar?q=${{encodeURIComponent(q)}}&sede=${{encodeURIComponent(sede)}}`)
    .then(r => r.json())
    .then(data => {{
        if (!data.length) {{
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
            const directorTip =
                `<strong>Correo:</strong> <a href="mailto:${{r.correo_director || ""}}">${{r.correo_director || "Sin info"}}</a><br>
                 <strong>Anexo:</strong> ${{r.anexo_director || "Sin info"}}<br>
                 <strong>Restricción:</strong> ${{r.consultar_antes_de_entregar_contactos || "Sin restricción"}}`;

            const secTip =
                `<strong>Correo:</strong> <a href="mailto:${{r.correo_secretaria || ""}}">${{r.correo_secretaria || "Sin info"}}</a><br>
                 <strong>Anexo:</strong> ${{r.anexo_secretaria || "Sin info"}}`;

            html += `<tr>
            <td>
              <span class="person"
               onclick="event.stopPropagation();showTooltip(event, '${{directorTip}}')">
               ${{r.nombre || ""}}
              </span>
            </td>
            <td>${{r.escuela || ""}}</td>
            <td>${{r.cargo || ""}}</td>
            <td>${{r.campus || ""}}</td>
            <td>
              <span class="person"
               onclick="event.stopPropagation();showTooltip(event, '${{secTip}}')">
               ${{r.secretaria || "Sin info"}}
              </span>
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
# API
# =========================
@app.route("/buscar")
def buscar_api():
    q = request.args.get("q","").lower()
    sede = request.args.get("sede","").lower()

    if len(q) < 2:
        return jsonify([])

    query = supabase.table("directorio_escuelas_umayor").select("*").or_(
        f"escuela.ilike.%{q}%,nombre.ilike.%{q}%,cargo.ilike.%{q}%"
    )

    if sede:
        query = query.ilike("sede", f"%{sede}%")

    res = query.execute()
    return jsonify(res.data or [])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



