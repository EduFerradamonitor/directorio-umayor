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
    margin-bottom: 25px;
}}

.logo-um {{
    height: 90px;
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

.tooltip-link {{
    color: #005baa;
    cursor: pointer;
    text-decoration: underline;
}}

.tooltip {{
    position: absolute;
    background: white;
    border: 1px solid #ccc;
    padding: 10px;
    font-size: 14px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    border-radius: 6px;
    z-index: 9999;
    max-width: 300px;
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

    <input id="busqueda"
           placeholder="¿Qué escuela busca? (ej: derecho, vet, psicología)"
           onkeydown="if(event.key==='Enter') buscar();">

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
let tooltip;

function cerrarTooltip() {{
    if (tooltip) {{
        tooltip.remove();
        tooltip = null;
    }}
}}

document.addEventListener("click", cerrarTooltip);

function mostrarTooltip(e, data) {{
    e.stopPropagation();
    cerrarTooltip();

    tooltip = document.createElement("div");
    tooltip.className = "tooltip";

    let html = "";

    if (data.correo) {{
        html += `<strong>Correo:</strong><br>
                 <a href="mailto:${{data.correo}}">${{data.correo}}</a><br><br>`;
    }}

    if (data.anexo) {{
        html += `<strong>Anexo:</strong> ${{data.anexo}}<br><br>`;
    }}

    if (data.restriccion) {{
        html += `<strong>Restricción:</strong><br>${{data.restriccion}}`;
    }}

    tooltip.innerHTML = html;

    document.body.appendChild(tooltip);

    tooltip.style.left = e.pageX + "px";
    tooltip.style.top = e.pageY + "px";
}}

function buscar() {{
    const q = document.getElementById("busqueda").value;
    const sede = document.getElementById("sede").value;

    fetch(`/buscar?q=${{encodeURIComponent(q)}}&sede=${{encodeURIComponent(sede)}}`)
    .then(r => r.json())
    .then(data => {{
        if (!data.length) {{
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
                    <span class="tooltip-link"
                          onclick='mostrarTooltip(event, {{
                              correo: "${{r.correo_director || ""}}",
                              anexo: "${{r.anexo_director || ""}}",
                              restriccion: "${{r.consultar_antes_de_entregar_contactos || ""}}"
                          }})'>
                        ${{r.nombre || ""}}
                    </span>
                </td>

                <td>${{r.escuela_busqueda || r.escuela || ""}}</td>
                <td>${{r.cargo || ""}}</td>
                <td>${{r.campus || ""}}</td>

                <td>
                    <span class="tooltip-link"
                          onclick='mostrarTooltip(event, {{
                              correo: "${{r.correo_secretaria || ""}}",
                              anexo: "${{r.anexo_secretaria || ""}}"
                          }})'>
                        ${{r.secretaria || "No informado"}}
                    </span>
                </td>

                <td>${{r.sede || ""}}</td>
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
# API BUSCADOR
# =========================
@app.route("/buscar")
def buscar_api():
    q = request.args.get("q", "").lower()
    sede = request.args.get("sede", "").lower()

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
        query = query.ilike("sede", sede)

    result = query.execute()
    return jsonify(result.data or [])

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)




