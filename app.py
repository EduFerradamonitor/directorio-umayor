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
    max-width: 1300px;
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
    table-layout: fixed;
}}

th, td {{
    border: 1px solid #ddd;
    padding: 8px;
    vertical-align: top;
}}

th {{
    background: #005baa;
    color: white;
}}

th:nth-child(1) {{ width: 15%; }}
th:nth-child(2) {{ width: 20%; }}
th:nth-child(3) {{ width: 18%; }}
th:nth-child(4) {{ width: 17%; }}
th:nth-child(5) {{ width: 15%; }}
th:nth-child(6) {{ width: 15%; }}

a.mail {{
    color: #005baa;
    text-decoration: underline;
    display: inline-block;
    max-width: 100%;
    word-break: break-all;
}}

.tooltip {{
    position: relative;
    display: inline-block;
}}

.tooltip-box {{
    visibility: hidden;
    width: 280px;
    background-color: #333;
    color: #fff;
    text-align: left;
    border-radius: 6px;
    padding: 10px;
    position: absolute;
    z-index: 999;
    bottom: 125%;
    left: 50%;
    transform: translateX(-50%);
    font-size: 13px;
    line-height: 1.4;
}}

.tooltip:hover .tooltip-box {{
    visibility: visible;
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
           placeholder="Buscar escuela, cargo o nombre"
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
function mailto(correo) {{
    if (!correo || correo === "no informado") return "No informado";
    return `<a class="mail" href="mailto:${{correo}}">${{correo}}</a>`;
}}

function textoRestriccion(texto) {{
    if (!texto) return "Sin información";
    return texto;
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
            <th>Nombre</th>
            <th>Escuela</th>
            <th>Cargo</th>
            <th>Campus</th>
            <th>Director</th>
            <th>Secretaría</th>
        </tr>`;

        data.forEach(r => {{
            html += `<tr>
                <td>${{r.nombre || ""}}</td>
                <td>${{r.escuela_busqueda || r.escuela || ""}}</td>
                <td>${{r.cargo || ""}}</td>
                <td>${{r.campus || ""}}</td>

                <td>
                    <span class="tooltip">
                        ${{mailto(r.correo_director)}}
                        <span class="tooltip-box">
                            <strong>Anexo director:</strong><br>
                            ${{r.anexo_director || "Sin información"}}<br><br>
                            <strong>Restricción:</strong><br>
                            ${{textoRestriccion(r.consultar_antes_de_entregar_contactos)}}
                        </span>
                    </span>
                </td>

                <td>
                    <span class="tooltip">
                        ${{mailto(r.correo_secretaria)}}
                        <span class="tooltip-box">
                            <strong>Secretaría:</strong> ${{r.secretaria || "Sin información"}}<br>
                            <strong>Anexo:</strong> ${{r.anexo_secretaria || "Sin información"}}<br><br>
                            <strong>Restricción:</strong><br>
                            ${{textoRestriccion(r.consultar_antes_de_entregar_contactos)}}
                        </span>
                    </span>
                </td>
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)




