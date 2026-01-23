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
    max-width: 1100px;
    margin: 30px auto;
    background: white;
    padding: 28px;
    border-radius: 12px;
    box-shadow: 0 0 20px rgba(0,0,0,0.1);
}}

.header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
}}

.logo-um {{
    height: 110px;
    object-fit: contain;
}}

input, select, button {{
    width: 100%;
    padding: 11px;
    margin: 8px 0;
    font-size: 15px;
}}

.filters {{
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 12px;
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
    margin-top: 18px;
    table-layout: fixed;
}}

th, td {{
    border: 1px solid #ddd;
    padding: 8px;
    vertical-align: top;
    font-size: 14px;
    word-wrap: break-word;
}}

th {{
    background: #005baa;
    color: white;
}}

th:nth-child(1),
th:nth-child(5) {{
    width: 18%;
}}

th:nth-child(2) {{
    width: 22%;
}}

th:nth-child(3),
th:nth-child(4),
th:nth-child(6) {{
    width: 10%;
}}

.person {{
    cursor: pointer;
    color: #005baa;
    text-decoration: underline;
}}

.tooltip {{
    display: none;
    position: absolute;
    background: #ffffff;
    border: 1px solid #ccc;
    padding: 10px;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    z-index: 1000;
    width: 260px;
    font-size: 13px;
}}

.tooltip strong {{
    display: block;
    margin-bottom: 4px;
}}

.footer {{
    margin-top: 26px;
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
        <img src="{url_for('static', filename='img/logoum.jpg')}"
             class="logo-um"
             alt="Universidad Mayor">
    </div>

    <div class="filters">
        <input id="busqueda"
               placeholder="Buscar escuela, director o cargo"
               onkeydown="if(event.key === 'Enter') buscar();">

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

function mostrarTooltip(event, html) {{
    tooltip.innerHTML = html;
    tooltip.style.display = "block";
    tooltip.style.top = (event.pageY + 10) + "px";
    tooltip.style.left = (event.pageX + 10) + "px";
}}

function ocultarTooltip() {{
    tooltip.style.display = "none";
}}

function buscar() {{
    const q = document.getElementById("busqueda").value;
    const sede = document.getElementById("sede").value;

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
            const directorTooltip = `
                <strong>Correo:</strong>
                <a href="mailto:${{r.correo_director || ""}}">${{r.correo_director || "Sin información"}}</a><br>
                <strong>Anexo:</strong> ${{r.anexo_director || "Sin información"}}<br>
                <strong>Restricción:</strong> ${{r.consultar_antes_de_entregar_contactos || "Sin restricción"}}
            `;

            const secretariaTooltip = `
                <strong>Correo:</strong>
                <a href="mailto:${{r.correo_secretaria || ""}}">${{r.correo_secretaria || "Sin información"}}</a><br>
                <strong>Anexo:</strong> ${{r.anexo_secretaria || "Sin información"}}
            `;

            html += `<tr>
                <td>
                    <span class="person"
                          onclick="event.stopPropagation(); mostrarTooltip(event, \`${{directorTooltip}}\`);">
                        ${{r.nombre || "Sin información"}}
                    </span>
                </td>
                <td>${{r.escuela_busqueda || r.escuela || ""}}</td>
                <td>${{r.cargo || ""}}</td>
                <td>${{r.campus || ""}}</td>
                <td>
                    <span class="person"
                          onclick="event.stopPropagation(); mostrarTooltip(event, \`${{secretariaTooltip}}\`);">
                        ${{r.secretaria || "Sin información"}}
                    </span>
                </td>
                <td>${{r.sede || ""}}</td>
            </tr>`;
        }});

        html += "</table>";
        document.getElementById("resultados").innerHTML = html;
    }})
    .catch(err => {{
        document.getElementById("resultados").innerHTML =
            "<p>Error al consultar los datos.</p>";
        console.error(err);
    }});
}}

function borrar() {{
    document.getElementById("busqueda").value = "";
    document.getElementById("sede").value = "";
    document.getElementById("resultados").innerHTML = "";
}}

document.addEventListener("click", ocultarTooltip);
</script>

</body>
</html>
"""

# =========================
# API BUSCADOR
# =========================
@app.route("/buscar")
def buscar_api():
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
        query = query.ilike("sede", f"%{sede}%")

    result = query.execute()
    return jsonify(result.data if result.data else [])

# =========================
# EJECUCIÓN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



