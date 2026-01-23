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
# CARÁTULA
# =========================
@app.route("/")
def home():
    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Directorio UM</title>
<style>
body {{
    font-family: Calibri, Arial, sans-serif;
    background:#f3f6f9;
}}
.card {{
    max-width:900px;
    margin:60px auto;
    background:white;
    padding:40px;
    border-radius:16px;
    text-align:center;
    box-shadow:0 0 25px rgba(0,0,0,.1);
}}
.logo {{
    width:70%;
    margin-bottom:20px;
}}
a.btn {{
    display:block;
    margin:15px auto;
    padding:14px;
    width:60%;
    background:#005baa;
    color:white;
    text-decoration:none;
    border-radius:10px;
    font-size:18px;
}}
.links a {{
    display:block;
    margin:6px 0;
    color:#005baa;
}}
.footer {{
    margin-top:30px;
    font-size:13px;
    color:#555;
}}
</style>
</head>
<body>
<div class="card">
<a href="https://www.umayor.cl/" target="_blank">
<img src="{url_for('static', filename='img/logoum.jpg')}" class="logo">
</a>

<a class="btn" href="/escuelas">📘 Directorio de Escuelas</a>
<a class="btn" href="/academicos">🎓 Otros Contactos Académicos</a>

<div class="links">
<h4>Links de interés</h4>
<a href="https://www.umayor.cl/um/servicios-estudiantiles/Registro-Estudiantes" target="_blank">ORE</a>
<a href="https://sso.umayor.cl/authentication/SignIn?SID=13&app_url=certificadosalumnos.umayor.cl" target="_blank">Portal de Certificados</a>
<a href="https://www.umayor.cl/um/servicios-estudiantiles/Gratuidad-Becas-y-ayudas-estudiantiles" target="_blank">Becas y Créditos</a>
<a href="https://www.umayor.cl/um/servicios-estudiantiles/Gestion-Financiera" target="_blank">Gestión Financiera</a>
<a href="https://www.umayor.cl/um/oferta-academica" target="_blank">Oferta Académica</a>
<a href="https://www.admisionmayor.cl/preguntas-frecuentes" target="_blank">Preguntas Frecuentes Admisión</a>
</div>

<div class="footer">
Desarrollado por <strong>Eduardo Ferrada</strong><br>
Universidad Mayor · Enero 2026
</div>
</div>
</body>
</html>
"""

# =========================
# DIRECTORIO DE ESCUELAS
# =========================
@app.route("/escuelas")
def escuelas():
    return render_directorio(
        titulo="📘 Directorio de Escuelas",
        api="/api/escuelas",
        placeholder="Buscar escuela (mínimo 3 letras)",
        mostrar_sede=True
    )

# =========================
# CONTACTOS ACADÉMICOS
# =========================
@app.route("/academicos")
def academicos():
    return render_directorio(
        titulo="🎓 Otros Contactos Académicos",
        api="/api/academicos",
        placeholder="Buscar por nombre (mínimo 3 letras)",
        mostrar_sede=False
    )

# =========================
# TEMPLATE BASE
# =========================
def render_directorio(titulo, api, placeholder, mostrar_sede):
    sede_html = """
    <select id="sede">
        <option value="">Todas las sedes</option>
        <option value="santiago">Santiago</option>
        <option value="temuco">Temuco</option>
    </select>
    """ if mostrar_sede else ""

    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>{titulo}</title>
<style>
body {{ font-family:Calibri, Arial; background:#f3f6f9; }}
.card {{ max-width:1100px; margin:40px auto; background:white;
padding:30px; border-radius:14px; box-shadow:0 0 20px rgba(0,0,0,.1); }}
.header {{ display:flex; justify-content:space-between; align-items:center; }}
.logo {{ height:70px; }}
.back {{ text-decoration:none; background:#e6e6e6; padding:8px 14px;
border-radius:8px; color:#333; }}
.info {{ margin:15px 0; padding:12px; background:#eef3f8;
font-size:17px; font-weight:bold; }}
input, select, button {{ width:100%; padding:12px; margin:8px 0; font-size:16px; }}
button {{ background:#005baa; color:white; border:none; cursor:pointer; }}
.secondary {{ background:#999; }}
table {{ width:100%; border-collapse:collapse; margin-top:20px; }}
th, td {{ border:1px solid #ddd; padding:8px; vertical-align:top; }}
th {{ background:#005baa; color:white; }}
.tooltip {{ cursor:pointer; position:relative; }}
.tooltip span {{ visibility:hidden; background:#333; color:#fff;
padding:10px; border-radius:6px; position:absolute; z-index:1;
top:20px; left:0; width:300px; }}
.tooltip:hover span {{ visibility:visible; }}
.footer {{ margin-top:30px; font-size:13px; color:#555; text-align:center; }}
</style>
</head>
<body>
<div class="card">
<div class="header">
<h2>{titulo}</h2>
<div>
<a href="/" class="back">⬅ Inicio</a>
<img src="{url_for('static', filename='img/logoum.jpg')}" class="logo">
</div>
</div>

<div class="info">
ℹ️ Al primer ingreso del día la carga puede demorar.
Si no ves resultados, espera o actualiza.
Pasa el mouse sobre ℹ️ para ver más información.
</div>

<input id="q" placeholder="{placeholder}"
onkeydown="if(event.key==='Enter') buscar();">

{sede_html}

<button onclick="buscar()">Buscar</button>
<button class="secondary" onclick="borrar()">Borrar</button>

<div id="resultados"></div>

<div class="footer">
Desarrollado por <strong>Eduardo Ferrada</strong><br>
Universidad Mayor · Enero 2026
</div>
</div>

<script>
function iconoRestriccion(txt) {{
    if (!txt) return "🟢 Libre";
    txt = txt.toLowerCase();
    if (txt.includes("validacion")) return "⚠️ Validación previa";
    if (txt.includes("autorizacion")) return "🔒 Autorización";
    if (txt.includes("solo")) return "🟡 Solo secretaría";
    return "🟠 Restricción";
}}

function buscar() {{
    const q = document.getElementById("q").value;
    const sedeEl = document.getElementById("sede");
    const sede = sedeEl ? sedeEl.value : "";

    fetch(`{api}?q=${{encodeURIComponent(q)}}&sede=${{encodeURIComponent(sede)}}`)
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
<td class="tooltip">${{r.nombre || ""}} ℹ️
<span>
<strong>Correo:</strong><br>
<a href="mailto:${{r["correo director"]}}">${{r["correo director"] || "—"}}</a><br>
<strong>Anexo:</strong> ${{r.anexo_director || "—"}}<br><br>
<strong>Restricción:</strong> ${{iconoRestriccion(r.consultar_antes_de_entregar_contactos)}}
</span>
</td>
<td>${{r.escuela_busqueda || r.escuela || ""}}</td>
<td>${{r.cargo || ""}}</td>
<td>${{r.campus || ""}}</td>
<td class="tooltip">${{r.secretaria_nombre || ""}} ℹ️
<span>
<a href="mailto:${{r.secretaria_correo}}">${{r.secretaria_correo || "—"}}</a><br>
Anexo: ${{r.anexo_secretaria || "—"}}
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
    document.getElementById("q").value="";
    if (document.getElementById("sede")) document.getElementById("sede").value="";
    document.getElementById("resultados").innerHTML="";
}}
</script>
</body>
</html>
"""

# =========================
# API ESCUELAS
# =========================
@app.route("/api/escuelas")
def api_escuelas():
    q = request.args.get("q","").lower()
    sede = request.args.get("sede","").lower()

    if len(q) < 3:
        return jsonify([])

    query = supabase.table("directorio_escuelas").select("*") \
        .or_(f"escuela_busqueda.ilike.%{q}%,nombre.ilike.%{q}%")

    if sede:
        query = query.ilike("sede", sede)

    return jsonify(query.execute().data or [])

# =========================
# API ACADÉMICOS
# =========================
@app.route("/api/academicos")
def api_academicos():
    q = request.args.get("q","").lower()
    if len(q) < 3:
        return jsonify([])

    return jsonify(
        supabase.table("otros_contactos_academicos")
        .select("*")
        .ilike("nombre_busca", f"%{q}%")
        .execute().data or []
    )

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

