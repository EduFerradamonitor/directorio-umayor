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
    border-radius: 14px;
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

.table-wrapper {{
    overflow-x: auto;
    margin-top: 25px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
}}

th, td {{
    border: 1px solid #ddd;
    padding: 10px;
    vertical-align: top;
    word-wrap: break-word;
}}

th {{
    background: #005baa;
    color: white;
}}

.col-director {{ width: 18%; }}
.col-escuela {{ width: 20%; }}
.col-cargo {{ width: 16%; }}
.col-campus {{ width: 14%; }}
.col-secretaria {{ width: 18%; }}
.col-sede {{ width: 8%; }}

.nombre-click {{
    color: #005baa;
    cursor: pointer;
    text-decoration: underline;
}}

.tooltip {{
    display: none;
    position: absolute;
    background: #ffffff;
    border: 1px solid #ccc;
    padding: 10px;
    border-radius: 6px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    font-size: 14px;
    max-width: 260px;
    z-index: 1000;
}}

.footer {{
    margin-top: 35px;
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
       placeholder="¿Qué escuela busca? (ej: vet, derecho, psicología)"
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

<div id="tooltip" class="tooltip"></div>

<script>
function mostrarTooltip(event, contenido) {{
    const tooltip = document.getElementById("tooltip");
    tooltip.innerHTML = contenido;
    tooltip.style.display = "block";
    tooltip.style.left = event.pageX + "px";
    tooltip.style.top = event.pageY + "px";
}}

document.addEventListener("click", function(e) {{
    if (!e.target.classList.contains("nombre-click")) {{
        document.getElementById("tooltip").style.display = "none";
    }}
}});

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

        let html = `<div class="table-wrapper"><table>
        <tr>
            <th class="col-director">Director</th>
            <th class="col-escuela">Escuela</th>
            <th class="col-cargo">Cargo</th>
            <th class="col-campus">Campus</th>
            <th class="col-secretaria">Secretaría</th>
            <th class="col-sede">Sede</th>
        </tr>`;

        data.forEach(r => {{
            const tooltipDirector = `
                <strong>Correo:</strong>
                <a href="mailto:${{r.correo_director || ""}}">${{r.correo_director || "Sin información"}}</a><br>
                <strong>Anexo:</strong> ${{r.anexo_director || "Sin información"}}<br>
                <strong>Restricción:</strong> ${{r.consultar_antes_de_entregar_contactos || "Sin información"}}
            `;

            const tooltipSecretaria = `
                <strong>Correo:</strong>
                <a href="mailto:${{r.correo_secretaria || ""}}">${{r.correo_secretaria || "Sin información"}}</a><br>
                <strong>Anexo:</strong> ${{r.anexo_secretaria || "Sin información"}}
            `;

            html += `<tr>
                <td class="col-director">
                    <span class="nombre-click"
                          onclick="event.stopPropagation(); mostrarTooltip(event, \`${{tooltipDirector}}\`)">
                        ${{r.nombre || ""}}
                    </span>
                </td>
                <td>${{r.escuela_busqueda || r.escuela || ""}}</td>
                <td>${{r.cargo || ""}}</td>
                <td>${{r.campus || ""}}</td>
                <td class="col-secretaria">
                    <span class="nombre-click"
                          onclick="event.stopPropagation(); mostrarTooltip(event, \`${{tooltipSecretaria}}\`)">
                        ${{r.secretaria || "Sin información"}}
                    </span>
                </td>
                <td>${{r.sede || ""}}</td>
            </tr>`;
        }});

        html += "</table></div>";
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
# API BUSQUEDA
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
        query = query.ilike("sede", sede)

    result = query.execute()
    return jsonify(result.data if result.data else [])

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


