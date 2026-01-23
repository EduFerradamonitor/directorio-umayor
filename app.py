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
# HOME / PORTADA
# =========================
@app.route("/")
def home():
    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Directorio General UMAYOR</title>

<style>
body {{
    font-family: Calibri, Arial, sans-serif;
    background: #f3f6f9;
}}

.card {{
    max-width: 1000px;
    margin: 40px auto;
    background: white;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 0 20px rgba(0,0,0,0.1);
    text-align: center;
}}

.logo {{
    height: 220px;
    margin-bottom: 20px;
}}

h1 {{
    margin-bottom: 30px;
}}

button {{
    padding: 14px 20px;
    margin: 10px;
    font-size: 16px;
    background: #005baa;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
}}

.acordeon {{
    margin-top: 30px;
    text-align: left;
}}

.acordeon summary {{
    cursor: pointer;
    font-weight: bold;
}}

.footer {{
    margin-top: 40px;
    font-size: 13px;
    color: #555;
}}
</style>
</head>

<body>
<div class="card">

<a href="https://www.umayor.cl" target="_blank">
<img src="{url_for('static', filename='img/logoum.jpg')}" class="logo">
</a>

<h1>Directorio General UMAYOR<br><small>Uso Interno SAT</small></h1>

<button onclick="location.href='/escuelas'">Directorio de Escuelas</button>
<button onclick="location.href='/academicos'">Otros Contactos Académicos</button>

<details class="acordeon">
<summary>Links de interés</summary>
<ul>
<li><a href="https://www.umayor.cl/um/servicios-estudiantiles/Registro-Estudiantes" target="_blank">ORE</a></li>
<li><a href="https://certificadosalumnos.umayor.cl" target="_blank">Portal de Certificados</a></li>
<li><a href="https://www.umayor.cl/um/servicios-estudiantiles/Gratuidad-Becas-y-ayudas-estudiantiles" target="_blank">Becas y Créditos</a></li>
<li><a href="https://www.umayor.cl/um/servicios-estudiantiles/Gestion-Financiera" target="_blank">Gestión Financiera</a></li>
<li><a href="https://www.umayor.cl/um/oferta-academica" target="_blank">Oferta Académica</a></li>
<li><a href="https://www.admisionmayor.cl/preguntas-frecuentes" target="_blank">Preguntas Frecuentes Admisión</a></li>
</ul>
</details>

<div class="footer">
Desarrollado por <strong>Eduardo Ferrada</strong> · Enero 2026
</div>

</div>
</body>
</html>
"""

# =========================
# DIRECTORIO ESCUELAS
# =========================
@app.route("/escuelas")
def escuelas():
    return render_busqueda(
        titulo="Directorio de Escuelas",
        endpoint="/api/escuelas"
    )

@app.route("/api/escuelas")
def api_escuelas():
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
            f"nombre.ilike.%{q}%,"
            f"cargo.ilike.%{q}%"
        )
    )

    if sede:
        query = query.ilike("sede", f"%{sede}%")

    return jsonify(query.execute().data or [])

# =========================
# OTROS CONTACTOS ACADÉMICOS
# =========================
@app.route("/academicos")
def academicos():
    return render_busqueda(
        titulo="Otros Contactos Académicos",
        endpoint="/api/academicos"
    )

@app.route("/api/academicos")
def api_academicos():
    q = request.args.get("q", "").strip().lower()

    if len(q) < 2:
        return jsonify([])

    query = (
        supabase
        .table("otros_contactos_academicos")
        .select("*")
        .ilike("nombre_busqueda", f"%{q}%")
    )

    return jsonify(query.execute().data or [])

# =========================
# PLANTILLA BUSCADOR
# =========================
def render_busqueda(titulo, endpoint):
    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>{titulo}</title>

<style>
body {{
    font-family: Calibri, Arial, sans-serif;
    background: #f3f6f9;
}}

.card {{
    max-width: 1100px;
    margin: 40px auto;
    background: white;
    padding: 30px;
    border-radius: 12px;
}}

input, select, button {{
    padding: 10px;
    margin: 5px;
    font-size: 15px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}}

th, td {{
    border: 1px solid #ddd;
    padding: 8px;
}}

th {{
    background: #005baa;
    color: white;
}}

.tooltip {{
    position: relative;
    cursor: help;
}}

.tooltip .tooltiptext {{
    visibility: hidden;
    background: #333;
    color: #fff;
    padding: 8px;
    border-radius: 6px;
    position: absolute;
    z-index: 1;
    width: 220px;
}}

.tooltip:hover .tooltiptext {{
    visibility: visible;
}}
</style>
</head>

<body>
<div class="card">

<h2>{titulo}</h2>

<p><strong>ℹ️ Al primer ingreso del día la carga puede demorar.  
Si no ves resultados de inmediato, espera o actualiza la página.  
Desliza el mouse sobre el ícono ℹ️ para ver más información.</strong></p>

<input id="q" placeholder="Buscar..." onkeydown="if(event.key==='Enter') buscar();">
<select id="sede">
<option value="">Todas</option>
<option value="santiago">Santiago</option>
<option value="temuco">Temuco</option>
</select>

<button onclick="buscar()">Buscar</button>
<button onclick="limpiar()">Limpiar</button>
<button onclick="location.href='/'">Volver al inicio</button>

<div id="resultados"></div>

</div>

<script>
function buscar() {{
    const q = document.getElementById("q").value;
    const sede = document.getElementById("sede").value;

    fetch(`{endpoint}?q=${{encodeURIComponent(q)}}&sede=${{encodeURIComponent(sede)}}`)
    .then(r => r.json())
    .then(data => {{
        if (!data.length) {{
            document.getElementById("resultados").innerHTML = "<p>No hay resultados.</p>";
            return;
        }}

        let html = "<table><tr><th>Nombre</th><th>Cargo</th><th>Correo</th></tr>";

        data.forEach(r => {{
            html += `<tr>
                <td class="tooltip">${{r.nombre || ""}}
                    <span class="tooltiptext">
                        Director: ${{r.correo_director || "Sin información"}}<br>
                        Secretaria: ${{r.secretaria_nombre || ""}}<br>
                        ${{r.secretaria_correo || ""}}
                    </span>
                </td>
                <td>${{r.cargo || ""}}</td>
                <td>${{r.correo_director || ""}}</td>
            </tr>`;
        }});

        html += "</table>";
        document.getElementById("resultados").innerHTML = html;
    });
}}

function limpiar() {{
    document.getElementById("q").value = "";
    document.getElementById("sede").value = "";
    document.getElementById("resultados").innerHTML = "";
}}
</script>

</body>
</html>
"""

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

