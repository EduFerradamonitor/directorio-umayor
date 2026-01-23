from flask import Flask, request, jsonify, url_for
from supabase import create_client

app = Flask(__name__)

# =========================
# CONFIGURACIÓN SUPABASE
# =========================
SUPABASE_URL = "https://wkbltctqqsuxqhlbnoeg.supabase.co"
SUPABASE_KEY = "PEGA_AQUI_TU_KEY_ANON_COMPLETA"

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
    margin-bottom: 20px;
}}

.logo-um {{
    height: 80px;
    object-fit: contain;
}}

.info-box {{
    display: flex;
    gap: 10px;
    align-items: flex-start;
    background: #f0f6ff;
    border-left: 5px solid #0b5ed7;
    padding: 14px 16px;
    margin-bottom: 25px;
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
    margin-top: 25px;
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

.info-icon {{
    display: inline-block;
    margin-left: 6px;
    background: #0b5ed7;
    color: white;
    border-radius: 4px;
    font-size: 12px;
    padding: 2px 6px;
    cursor: pointer;
}}

.tooltip {{
    display: none;
    position: absolute;
    background: white;
    border: 1px solid #ccc;
    padding: 10px;
    border-radius: 6px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    font-size: 14px;
    z-index: 1000;
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

    <input id="busqueda"
           placeholder="¿Qué escuela busca? (ej: derecho, psicología)"
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
let tooltip = document.getElementById("tooltip");

document.addEventListener("click", () => {{
    tooltip.style.display = "none";
}});

function mostrarTooltip(event, html) {{
    event.stopPropagation();
    tooltip.innerHTML = html;
    tooltip.style.display = "block";
    tooltip.style.left = event.pageX + "px";
    tooltip.style.top = event.pageY + "px";
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
            html += `<tr>
                <td>
                    ${{r.nombre || ""}}
                    <span class="info-icon"
                        onclick="mostrarTooltip(event,
                        '<strong>Correo:</strong> <a href=mailto:${{r.correo_director}}>${{r.correo_director || "No informado"}}</a><br>\
                         <strong>Anexo:</strong> ${{r.anexo_director || "Sin información"}}')">ℹ️</span>
                </td>
                <td>${{r.escuela_busqueda || ""}}</td>
                <td>${{r.cargo || ""}}</td>
                <td>${{r.campus || ""}}</td>
                <td>
                    ${{r.secretaria || "No informado"}}
                    <span class="info-icon"
                        onclick="mostrarTooltip(event,
                        '<strong>Correo:</strong> <a href=mailto:${{r.correo_secretaria}}>${{r.correo_secretaria || "No informado"}}</a><br>\
                         <strong>Anexo:</strong> ${{r.anexo_secretaria || "Sin información"}}')">ℹ️</span>
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
            f"nombre.ilike.%{q}%,"
            f"cargo.ilike.%{q}%"
        )
    )

    if sede:
        query = query.ilike("sede", sede)

    result = query.execute()
    return jsonify(result.data or [])

# =========================
# EJECUCIÓN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)






