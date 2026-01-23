from flask import Flask, request, jsonify, url_for
from supabase import create_client

app = Flask(__name__)

# =========================
# CONFIGURACIÓN SUPABASE
# =========================
SUPABASE_URL = "https://wkbltctqqsuxqhlbnoeg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndrYmx0Y3RxcXN1eHFobGJub2VnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjkwMDI1NzYsImV4cCI6MjA4NDU3ODU3Nn0.QLl8XI79jOC_31RjtTMCwrKAXNg-Y1Bt_x2JQL9rnEM"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ======================================================
# CARÁTULA / HOME
# ======================================================
@app.route("/")
def home():
    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Directorios UM</title>

<style>
body {{
    font-family: Calibri, Arial, sans-serif;
    background: #f3f6f9;
}}

.card {{
    max-width: 900px;
    margin: 60px auto;
    background: white;
    padding: 40px;
    border-radius: 14px;
    box-shadow: 0 0 20px rgba(0,0,0,0.1);
    text-align: center;
}}

.logo {{
    width: 70%;
    max-width: 420px;
    margin-bottom: 30px;
}}

h1 {{
    margin-bottom: 10px;
}}

p {{
    color: #555;
}}

.menu {{
    margin-top: 40px;
}}

.menu a {{
    display: block;
    padding: 16px;
    margin: 15px 0;
    background: #005baa;
    color: white;
    text-decoration: none;
    border-radius: 10px;
    font-size: 18px;
}}

.menu a:hover {{
    background: #004a8f;
}}

.links {{
    margin-top: 35px;
    text-align: left;
}}

.links summary {{
    font-weight: bold;
    cursor: pointer;
}}

.links a {{
    display: block;
    margin: 8px 0;
    color: #005baa;
    text-decoration: none;
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

<a href="https://www.umayor.cl/" target="_blank">
    <img src="{url_for('static', filename='img/logoum.jpg')}" class="logo">
</a>

<h1>Directorios Internos UM</h1>
<p>Acceso centralizado a información institucional</p>

<div class="menu">
    <a href="/escuelas">📘 Directorio de Escuelas</a>
    <a href="/academicos">🎓 Otros Contactos Académicos</a>
</div>

<details class="links">
<summary>🔗 Links de interés</summary>
<a href="https://www.umayor.cl/um/servicios-estudiantiles/Registro-Estudiantes" target="_blank">ORE</a>
<a href="https://sso.umayor.cl/authentication/SignIn?SID=13&app_url=certificadosalumnos.umayor.cl" target="_blank">Portal de Certificados</a>
<a href="https://www.umayor.cl/um/servicios-estudiantiles/Gratuidad-Becas-y-ayudas-estudiantiles" target="_blank">Becas y Créditos</a>
<a href="https://www.umayor.cl/um/servicios-estudiantiles/Gestion-Financiera" target="_blank">Gestión Financiera</a>
<a href="https://www.umayor.cl/um/oferta-academica" target="_blank">Oferta Académica</a>
<a href="https://www.admisionmayor.cl/preguntas-frecuentes" target="_blank">Preguntas Frecuentes Admisión</a>
</details>

<div class="footer">
Desarrollado por <strong>Eduardo Ferrada</strong><br>
Universidad Mayor · Enero 2026
</div>

</div>
</body>
</html>
"""

# ======================================================
# MÓDULO: OTROS CONTACTOS ACADÉMICOS
# ======================================================
@app.route("/academicos")
def academicos():
    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Otros Contactos Académicos</title>

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
    box-shadow: 0 0 20px rgba(0,0,0,0.1);
}}

.header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.logo {{
    height: 80px;
}}

.info {{
    margin: 15px 0;
    padding: 10px;
    background: #eef3f8;
    font-size: 15px;
    font-weight: bold;
}}

input, button {{
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

table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
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

.tooltip {{
    position: relative;
    cursor: pointer;
}}

.tooltip span {{
    visibility: hidden;
    background: #333;
    color: #fff;
    padding: 8px;
    border-radius: 6px;
    position: absolute;
    z-index: 1;
    top: 20px;
    left: 0;
    width: 260px;
}}

.tooltip:hover span {{
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
<h2>🎓 Otros Contactos Académicos</h2>
<img src="{url_for('static', filename='img/logoum.jpg')}" class="logo">
</div>

<div class="info">
ℹ️ Al primer ingreso del día, la carga puede demorar unos segundos.
Si no ves resultados de inmediato, espera o actualiza la página.
Pasa el mouse sobre el ícono ℹ️ para ver más información.
</div>

<input id="q" placeholder="Buscar por nombre (mínimo 3 letras)" onkeydown="if(event.key==='Enter') buscar();">
<button onclick="buscar()">Buscar</button>

<div id="resultados"></div>

<div class="footer">
Desarrollado por <strong>Eduardo Ferrada</strong><br>
Universidad Mayor · Enero 2026
</div>

</div>

<script>
function buscar() {{
    const q = document.getElementById("q").value;

    fetch(`/buscar_academicos?q=${{encodeURIComponent(q)}}`)
    .then(r => r.json())
    .then(data => {{
        if (!data || data.length === 0) {{
            document.getElementById("resultados").innerHTML = "<p>No se encontraron resultados.</p>";
            return;
        }}

        let html = `<table>
        <tr>
            <th>Académico</th>
            <th>Cargo</th>
            <th>Contacto</th>
            <th>Restricción</th>
        </tr>`;

        data.forEach(r => {{
            html += `<tr>
                <td>${{r.nombre}}</td>
                <td>${{r.cargo || ""}}</td>
                <td class="tooltip">ℹ️
                    <span>
                    <strong>Correo:</strong> <a href="mailto:${{r.correo_director}}">${{r.correo_director}}</a><br>
                    <strong>Secretaría:</strong> ${{r.secretaria_nombre || "Sin información"}}<br>
                    <strong>Correo Secretaría:</strong> ${{r.secretaria_correo || "—"}}
                    </span>
                </td>
                <td>${{r.consultar_antes_de_entregar_contactos || ""}}</td>
            </tr>`;
        }});

        html += "</table>";
        document.getElementById("resultados").innerHTML = html;
    }});
}}
</script>

</body>
</html>
"""

# ======================================================
# API: BUSCAR ACADÉMICOS
# ======================================================
@app.route("/buscar_academicos")
def buscar_academicos():
    q = request.args.get("q", "").strip().lower()

    if len(q) < 3:
        return jsonify([])

    result = (
        supabase
        .table("otros_contactos_academicos")
        .select("*")
        .ilike("nombre_busqueda", f"%{q}%")
        .execute()
    )

    return jsonify(result.data if result.data else [])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
