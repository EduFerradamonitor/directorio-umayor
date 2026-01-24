from flask import Flask, request, jsonify, url_for, render_template
from supabase import create_client

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("home.html")

# =========================
# SUPABASE
# =========================
SUPABASE_URL = "https://wkbltctqqsuxqhlbnoeg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndrYmx0Y3RxcXN1eHFobGJub2VnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjkwMDI1NzYsImV4cCI6MjA4NDU3ODU3Nn0.QLl8XI79jOC_31RjtTMCwrKAXNg-Y1Bt_x2JQL9rnEM"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# =========================
# PORTADA
# =========================
@app.route("/")
def home():
    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Directorio General Umayor</title>

<style>
body {{
    font-family: Calibri, Arial, sans-serif;
    background: #f3f6f9;
}}

.container {{
    max-width: 1100px;
    margin: 40px auto;
    background: white;
    padding: 40px;
    border-radius: 12px;
    box-shadow: 0 0 20px rgba(0,0,0,0.1);
    text-align: center;
}}

.logo {{
    max-height: 230px;
}}

.linea-amarilla {{
    height: 6px;
    background: #f2a900;
    margin: 20px 0 30px;
}}

.btn {{
    display: inline-block;
    margin: 10px;
    padding: 14px 28px;
    background: #005baa;
    color: white;
    text-decoration: none;
    border-radius: 6px;
}}

details {{
    margin-top: 30px;
    text-align: left;
}}

footer {{
    margin-top: 40px;
    font-size: 13px;
    color: #555;
}}
</style>
</head>

<body>
<div class="container">

<a href="https://www.umayor.cl/" target="_blank">
<img src="{url_for('static', filename='img/logoum.jpg')}" class="logo">
</a>

<div class="linea-amarilla"></div>

<h1>Directorio General Umayor</h1>
<p>Uso exclusivo SAT</p>

<a class="btn" href="/escuelas">Directorio de Escuelas</a>
<a class="btn" href="/academicos">Otros Contactos Académicos</a>

<details>
<summary>🔗 Links de uso frecuente</summary>
<ul>
<li><a href="https://www.umayor.cl/um/servicios-estudiantiles/Registro-Estudiantes" target="_blank">ORE</a></li>
<li><a href="https://www.umayor.cl/um/oferta-academica" target="_blank">Oferta Académica</a></li>
</ul>
</details>

<footer>
Desarrollado por <strong>Eduardo Ferrada</strong> · Enero 2026
</footer>

</div>
</body>
</html>
"""

# =========================
# ESCUELAS
# =========================
@app.route("/escuelas")
def escuelas():
    return plantilla_busqueda("Directorio de Escuelas", "/api/escuelas", True)

@app.route("/api/escuelas")
def api_escuelas():
    q = request.args.get("q", "").lower().strip()
    sede = request.args.get("sede", "").lower().strip()

    if len(q) < 2:
        return jsonify([])

    query = supabase.table("directorio_escuelas_umayor").select("*") \
        .or_(f"escuela_busqueda.ilike.%{q}%,nombre.ilike.%{q}%,cargo.ilike.%{q}%")

    if sede:
        query = query.ilike("sede", sede)

    return jsonify(query.execute().data or [])

# =========================
# ACADÉMICOS
# =========================
@app.route("/academicos")
def academicos():
    return plantilla_busqueda("Otros Contactos Académicos", "/api/academicos", False)

@app.route("/api/academicos")
def api_academicos():
    q = request.args.get("q", "").lower().strip()

    if len(q) < 2:
        return jsonify([])

    query = supabase.table("otros_contactos_academicos").select("*") \
        .or_(f"nombre_busqueda.ilike.%{q}%,cargo.ilike.%{q}%")

    return jsonify(query.execute().data or [])

# =========================
# PLANTILLA
# =========================
def plantilla_busqueda(titulo, endpoint, con_sede):
    sede_html = """
    <select id="sede">
        <option value="">Todas las sedes</option>
        <option value="santiago">Santiago</option>
        <option value="temuco">Temuco</option>
    </select>
    """ if con_sede else ""

    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{titulo}</title>

<style>
body {{ font-family: Calibri; background:#f3f6f9; }}
.card {{ max-width:1200px; margin:40px auto; background:white; padding:30px; border-radius:12px; }}

input {{ width:60%; padding:12px; }}
button, select {{ padding:12px; }}

table {{ width:100%; border-collapse:collapse; margin-top:20px; }}
th, td {{ border:1px solid #ddd; padding:8px; }}

.tooltip {{
    position: relative;
    cursor: pointer;
}}

.tooltip .tooltiptext {{
    visibility: hidden;
    background: #333;
    color: #fff;
    padding: 10px;
    border-radius: 6px;
    position: absolute;
    z-index: 10;
    top: 20px;
    left: 0;
    width: 260px;
}}

.tooltip:hover .tooltiptext {{
    visibility: visible;
}}

.copy {{
    cursor:pointer;
    margin-left:6px;
}}
</style>
</head>

<body>
<div class="card">

<a href="/"><button>⬅ Volver al inicio</button></a>
<h1>{titulo}</h1>

<p><strong>ℹ️ Al primer ingreso del día, la carga puede demorar unos segundos.</strong></p>

<input id="q" placeholder="Buscar..." onkeydown="if(event.key==='Enter')buscar();">
{sede_html}
<button onclick="buscar()">Buscar</button>
<button onclick="limpiar()">Borrar</button>

<div id="res"></div>

<footer style="margin-top:30px;font-size:13px;color:#555;">
Desarrollado por <strong>Eduardo Ferrada</strong> · Enero 2026
</footer>

</div>

<script>
function copiar(txt) {{
    navigator.clipboard.writeText(txt);
    alert("Correo copiado");
}}

function buscar() {{
    const q = document.getElementById("q").value;
    const sede = document.getElementById("sede") ? document.getElementById("sede").value : "";
    fetch("{endpoint}?q="+encodeURIComponent(q)+"&sede="+encodeURIComponent(sede))
    .then(r=>r.json())
    .then(d=>{{
        let h="<table><tr><th>Nombre</th><th>Cargo</th><th>Correo</th><th>ℹ️</th></tr>";
        d.forEach(r=>{{
            h+=`<tr>
<td>${{r.nombre||""}}</td>
<td>${{r.cargo||""}}</td>
<td>
<a href="mailto:${{r.correo_director||""}}">${{r.correo_director||""}}</a>
<span class="copy" onclick="copiar('${{r.correo_director||""}}')">📋</span>
</td>
<td class="tooltip">ℹ️
<div class="tooltiptext">
<b>Anexo director:</b> ${{r.anexo_director||"Sin info"}}<br>
<b>Restricción:</b> ${{r.consultar_antes_de_entregar_contactos||"—"}}
</div>
</td>
</tr>`;
        }});
        h+="</table>";
        document.getElementById("res").innerHTML=h;
    });
}}

function limpiar() {{
    document.getElementById("q").value="";
    document.getElementById("res").innerHTML="";
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


