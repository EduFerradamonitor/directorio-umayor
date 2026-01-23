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
# UTIL
# =========================
def badge_restriccion(texto):
    if not texto:
        return "🟢 Sin restricción"
    t = texto.lower()
    if "solo correo" in t:
        return "🟢 Solo correo secretaría"
    if "validacion" in t:
        return "🟠 Validación previa"
    if "autorizacion" in t:
        return "🔴 Autorización expresa"
    return "🟡 Información sensible"

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
}}
.logo {{
    text-align: center;
}}
.logo img {{
    height: 220px;
}}
.linea {{
    height: 6px;
    background: #f2b705;
    margin: 20px 0 30px 0;
}}
h1 {{
    text-align: center;
    margin-bottom: 5px;
}}
.subtitle {{
    text-align: center;
    color: #555;
    margin-bottom: 30px;
}}
.links {{
    margin-bottom: 30px;
}}
.links summary {{
    cursor: pointer;
    font-weight: bold;
}}
.links a {{
    display: block;
    margin: 6px 0;
}}
.buttons {{
    display: flex;
    gap: 20px;
    justify-content: center;
}}
button {{
    padding: 14px 30px;
    font-size: 16px;
    cursor: pointer;
    background: #005baa;
    color: white;
    border: none;
    border-radius: 6px;
}}
.footer {{
    margin-top: 40px;
    text-align: center;
    font-size: 13px;
    color: #555;
}}
.info {{
    font-weight: bold;
    font-size: 15px;
    margin-bottom: 20px;
}}
</style>
</head>
<body>
<div class="container">

<div class="logo">
<a href="https://www.umayor.cl" target="_blank">
<img src="{url_for('static', filename='img/logoum.jpg')}">
</a>
</div>

<div class="linea"></div>

<h1>Directorio General Umayor</h1>
<div class="subtitle">Uso interno – Servicio de Atención a Estudiantes</div>

<div class="info">
ℹ️ Al primer ingreso del día la carga puede demorar unos segundos.  
Si no ves el buscador de inmediato, espera o actualiza la página.  
Haz clic en el ícono ℹ️ para ver más información.
</div>

<details class="links">
<summary>🔗 Links de uso frecuente</summary>
<a href="https://www.umayor.cl/um/servicios-estudiantiles/Registro-Estudiantes" target="_blank">ORE</a>
<a href="https://certificadosalumnos.umayor.cl" target="_blank">Portal de Certificados</a>
<a href="https://www.umayor.cl/um/servicios-estudiantiles/Gratuidad-Becas-y-ayudas-estudiantiles" target="_blank">Becas y Créditos</a>
<a href="https://www.umayor.cl/um/servicios-estudiantiles/Gestion-Financiera" target="_blank">Gestión Financiera</a>
<a href="https://www.umayor.cl/um/oferta-academica" target="_blank">Oferta Académica</a>
<a href="https://www.admisionmayor.cl/preguntas-frecuentes" target="_blank">Preguntas Frecuentes Admisión</a>
</details>

<div class="buttons">
<a href="/escuelas"><button>Directorio de Escuelas</button></a>
<a href="/academicos"><button>Otros Contactos Académicos</button></a>
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
# DIRECTORIO ESCUELAS
# =========================
@app.route("/escuelas")
def escuelas():
    return pagina_busqueda(
        titulo="Directorio de Escuelas",
        endpoint="/api/escuelas"
    )

@app.route("/api/escuelas")
def api_escuelas():
    q = request.args.get("q", "").lower()
    sede = request.args.get("sede", "").lower()

    if len(q) < 3:
        return jsonify([])

    query = supabase.table("directorio_escuelas_umayor").select("*") \
        .ilike("escuela_busqueda", f"%{q}%")

    if sede:
        query = query.ilike("sede", sede)

    return jsonify(query.execute().data or [])

# =========================
# OTROS ACADEMICOS
# =========================
@app.route("/academicos")
def academicos():
    return pagina_busqueda(
        titulo="Otros Contactos Académicos",
        endpoint="/api/academicos",
        academicos=True
    )

@app.route("/api/academicos")
def api_academicos():
    q = request.args.get("q", "").lower()
    if len(q) < 3:
        return jsonify([])

    query = supabase.table("otros_contactos_academicos").select("*") \
        .ilike("nombre_busqueda", f"%{q}%")

    return jsonify(query.execute().data or [])

# =========================
# TEMPLATE BUSQUEDA
# =========================
def pagina_busqueda(titulo, endpoint, academicos=False):
    columna_extra = "<th>Departamento</th>" if academicos else ""
    columna_extra_td = "<td>"+("{r.departamento}" if academicos else "")+"</td>"

    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>{titulo}</title>
<style>
body {{ font-family: Calibri, Arial; background:#f3f6f9; }}
.container {{ max-width:1200px; margin:30px auto; background:white; padding:30px; border-radius:12px; }}
.header {{ display:flex; justify-content:space-between; align-items:center; }}
.header img {{ height:80px; }}
input {{ width:60%; padding:12px; }}
button {{ padding:12px 20px; margin-left:10px; }}
table {{ width:100%; border-collapse:collapse; margin-top:20px; }}
th,td {{ border:1px solid #ddd; padding:8px; }}
.tooltip {{ cursor:pointer; }}
.footer {{ margin-top:30px; text-align:center; font-size:13px; color:#555; }}
</style>
</head>
<body>
<div class="container">

<div class="header">
<h2>{titulo}</h2>
<img src="{url_for('static', filename='img/logoum.jpg')}">
</div>

<input id="q" placeholder="Escribe al menos 3 letras" onkeydown="if(event.key==='Enter') buscar()">
<button onclick="buscar()">Buscar</button>
<button onclick="limpiar()">Limpiar</button>
<button onclick="window.location='/'">Volver al inicio</button>

<div id="res"></div>

<div class="footer">
Desarrollado por <strong>Eduardo Ferrada</strong> · Universidad Mayor · Enero 2026
</div>

</div>

<script>
function buscar() {{
fetch("{endpoint}?q="+encodeURIComponent(q.value))
.then(r=>r.json())
.then(d=>{
if(!d.length){{res.innerHTML="Sin resultados";return;}}
let h="<table><tr><th>Nombre</th><th>Cargo</th><th>Correo Director</th><th>Secretaria</th><th>Correo Secretaria</th>{columna_extra}<th>ℹ️</th></tr>";
d.forEach(r=>{
h+="<tr>"+
"<td>"+(r.nombre||"")+"</td>"+
"<td>"+(r.cargo||"")+"</td>"+
"<td><a href='mailto:"+ (r.correo_director||"") +"'>"+(r.correo_director||"")+"</a></td>"+
"<td>"+(r.secretaria||r.secretaria_nombre||"")+"</td>"+
"<td><a href='mailto:"+ (r.correo_secretaria||r.secretaria_correo||"") +"'>"+(r.correo_secretaria||r.secretaria_correo||"")+"</a></td>"+
"{columna_extra_td}"+
"<td class='tooltip' title='Anexo director: "+(r.anexo_director||"Sin info")+" | Anexo secretaria: "+(r.anexo_secretaria||"Sin info")+" | "+(r.consultar_antes_de_entregar_contactos||"")+"'>ℹ️</td>"+
"</tr>";
});
h+="</table>";
res.innerHTML=h;
});
}
function limpiar(){{q.value="";res.innerHTML="";}}
</script>

</body>
</html>
"""
