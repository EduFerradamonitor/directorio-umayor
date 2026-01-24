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
    max-height: 260px;
}}

.linea-amarilla {{
    height: 6px;
    background: #f2a900;
    margin: 20px 0 30px 0;
}}

h1 {{
    margin-bottom: 10px;
}}

.subtitle {{
    color: #555;
    margin-bottom: 30px;
}}

.btn {{
    display: inline-block;
    margin: 10px;
    padding: 14px 28px;
    background: #005baa;
    color: white;
    text-decoration: none;
    border-radius: 6px;
    font-size: 16px;
}}

.btn:hover {{
    background: #004080;
}}

details {{
    margin-top: 30px;
    text-align: left;
}}

summary {{
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
<div class="container">

<a href="https://www.umayor.cl/" target="_blank">
<img src="{url_for('static', filename='img/logoum.jpg')}" class="logo">
</a>

<div class="linea-amarilla"></div>

<h1>Directorio General Umayor</h1>
<div class="subtitle">Uso exclusivo SAT</div>

<a href="/escuelas" class="btn">Directorio de Escuelas</a>
<a href="/academicos" class="btn">Otros Contactos Académicos</a>

<details>
<summary>🔗 Links de uso frecuente</summary>
<ul>
<li><a href="https://www.umayor.cl/um/servicios-estudiantiles/Registro-Estudiantes" target="_blank">ORE</a></li>
<li><a href="https://sso.umayor.cl/authentication/SignIn?SID=13&app_url=certificadosalumnos.umayor.cl" target="_blank">Portal de Certificados</a></li>
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
    return plantilla_busqueda(
        titulo="Directorio de Escuelas",
        endpoint="/api/escuelas",
        mostrar_sede=True,
        columna_extra=""
    )

@app.route("/api/escuelas")
def api_escuelas():
    q = request.args.get("q", "").lower().strip()
    sede = request.args.get("sede", "").lower().strip()

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

    return jsonify(query.execute().data or [])

# =========================
# OTROS CONTACTOS ACADÉMICOS
# =========================
@app.route("/academicos")
def academicos():
    return plantilla_busqueda(
        titulo="Otros Contactos Académicos",
        endpoint="/api/academicos",
        mostrar_sede=False,
        columna_extra="<th>Departamento</th>"
    )

@app.route("/api/academicos")
def api_academicos():
    q = request.args.get("q", "").lower().strip()

    if len(q) < 2:
        return jsonify([])

    query = (
        supabase
        .table("otros_contactos_academicos")
        .select("*")
        .or_(
            f"nombre_busqueda.ilike.%{q}%,"
            f"cargo.ilike.%{q}%"
        )
    )

    return jsonify(query.execute().data or [])

# =========================
# PLANTILLA REUTILIZABLE
# =========================
def plantilla_busqueda(titulo, endpoint, mostrar_sede, columna_extra):
    sede_html = ""
    if mostrar_sede:
        sede_html = """
        <select id="sede">
            <option value="">Todas las sedes</option>
            <option value="santiago">Santiago</option>
            <option value="temuco">Temuco</option>
        </select>
        """

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
    max-width: 1200px;
    margin: 40px auto;
    background: white;
    padding: 30px;
    border-radius: 12px;
}}

input {{
    width: 60%;
    padding: 12px;
}}

select, button {{
    padding: 12px;
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

.info {{
    cursor: pointer;
}}
</style>
</head>

<body>
<div class="card">

<a href="/"><button>⬅ Volver al inicio</button></a>

<h1>{titulo}</h1>

<p><strong>ℹ️ Al primer ingreso del día, la carga puede demorar unos segundos.  
Haz clic en el ícono ℹ️ para ver anexos y restricciones.</strong></p>

<input id="q" placeholder="Buscar..." onkeydown="if(event.key==='Enter')buscar();">
{sede_html}
<button onclick="buscar()">Buscar</button>
<button onclick="limpiar()">Borrar</button>

<div id="res"></div>

<p style="margin-top:30px;font-size:13px;color:#555;">
Desarrollado por <strong>Eduardo Ferrada</strong> · Enero 2026
</p>

</div>

<script>
function buscar() {{
    const q = document.getElementById("q").value;
    const sede = document.getElementById("sede") ? document.getElementById("sede").value : "";
    fetch("{endpoint}?q=" + encodeURIComponent(q) + "&sede=" + encodeURIComponent(sede))
    .then(r => r.json())
    .then(d => {{
        const res = document.getElementById("res");
        if(!d.length){{
            res.innerHTML = "Sin resultados";
            return;
        }}

        let h = "<table><tr><th>Nombre</th><th>Cargo</th><th>Correo Director</th><th>Secretaria</th><th>Correo Secretaria</th>{columna_extra}<th>ℹ️</th></tr>";

        d.forEach(r => {{
            h += "<tr>" +
                 "<td>" + (r.nombre || "") + "</td>" +
                 "<td>" + (r.cargo || "") + "</td>" +
                 "<td><a href='mailto:" + (r.correo_director || "") + "'>" + (r.correo_director || "") + "</a></td>" +
                 "<td>" + (r.secretaria_nombre || r.secretaria || "") + "</td>" +
                 "<td><a href='mailto:" + (r.secretaria_correo || "") + "'>" + (r.secretaria_correo || "") + "</a></td>" +
                 "{'<td>' + (r.departamento || '') + '</td>' if columna_extra else ''}" +
                 "<td class='info' onclick=\\"alert('Anexo director: ' + (r.anexo_director || 'Sin info') + '\\nAnexo secretaria: ' + (r.anexo_secretaria || 'Sin info') + '\\n' + (r.consultar_antes_de_entregar_contactos || ''))\\">ℹ️</td></tr>";
        }});

        h += "</table>";
        res.innerHTML = h;
    }});
}}

function limpiar() {{
    document.getElementById("q").value = "";
    document.getElementById("res").innerHTML = "";
}}
</script>

</body>
</html>
"""

# =========================
# EJECUCIÓN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
