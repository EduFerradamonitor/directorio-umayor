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
<title>Directorio UMAYOR</title>
<style>
body {{ font-family: Calibri, Arial; background:#f3f6f9; }}
.card {{ max-width:1100px; margin:40px auto; background:white; padding:40px; border-radius:14px; box-shadow:0 0 20px rgba(0,0,0,.1); text-align:center; }}
.logo {{ max-width:75%; margin-bottom:30px; }}
.modulos {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:20px; }}
.modulo {{ background:#005baa; color:white; padding:25px; border-radius:12px; font-size:18px; text-decoration:none; font-weight:bold; }}
.modulo:hover {{ background:#004080; }}
.footer {{ margin-top:40px; font-size:13px; color:#555; }}
</style>
</head>
<body>
<div class="card">
<a href="https://www.umayor.cl/" target="_blank">
<img src="{url_for('static', filename='img/logoum.jpg')}" class="logo">
</a>

<div class="modulos">
<a class="modulo" href="/escuelas">📘 Directorio de Escuelas</a>
<a class="modulo" href="/academicos">🎓 Otros Contactos Académicos</a>
</div>

<div class="footer">
Desarrollado por <strong>Eduardo Ferrada</strong> · Enero 2026
</div>
</div>
</body>
</html>
"""

# =========================
# VISTAS
# =========================
@app.route("/escuelas")
def escuelas():
    return "<script>location.href='/directorio/escuelas'</script>"

@app.route("/academicos")
def academicos():
    return "<script>location.href='/directorio/academicos'</script>"

# =========================
# API ESCUELAS (sin cambios)
# =========================
@app.route("/api/escuelas")
def api_escuelas():
    q = request.args.get("q","").lower().strip()
    sede = request.args.get("sede","").lower().strip()

    if len(q) < 3:
        return jsonify([])

    query = (
        supabase
        .table("directorio_escuelas_umayor")
        .select("*")
        .or_(f"escuela_busqueda.ilike.%{q}%,nombre.ilike.%{q}%,cargo.ilike.%{q}%")
    )

    if sede:
        query = query.ilike("sede", sede)

    return jsonify(query.execute().data or [])

# =========================
# API OTROS CONTACTOS ACADÉMICOS (PASO 4)
# =========================
@app.route("/api/academicos")
def api_academicos():
    q = request.args.get("q","").lower().strip()

    if len(q) < 3:
        return jsonify([])

    result = (
        supabase
        .table("otros_contactos_academicos")
        .select("*")
        .ilike("nombre_busqueda", f"%{q}%")
        .execute()
    )

    return jsonify(result.data or [])

# =========================
# DIRECTORIO ACADÉMICOS (UI + TOOLTIP)
# =========================
@app.route("/directorio/academicos")
def directorio_academicos():
    return """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Otros Contactos Académicos</title>

<style>
body { font-family: Calibri, Arial; background:#f3f6f9; }
.card { max-width:1100px; margin:40px auto; background:white; padding:30px; border-radius:12px; }
input, button { padding:10px; font-size:15px; }
table { width:100%; border-collapse:collapse; margin-top:20px; }
th, td { border:1px solid #ddd; padding:8px; vertical-align:top; }
th { background:#005baa; color:white; }

.info { position:relative; cursor:help; font-weight:bold; }
.tooltip {
    display:none;
    position:absolute;
    background:#333;
    color:white;
    padding:10px;
    border-radius:6px;
    top:20px;
    left:0;
    width:260px;
    z-index:10;
    font-size:13px;
}
.info:hover .tooltip { display:block; }

.ok { color:green; }
.warn { color:orange; }
.lock { color:red; }
</style>
</head>

<body>
<div class="card">
<h2>🎓 Otros Contactos Académicos</h2>

<input id="q" placeholder="Buscar por nombre">
<button onclick="buscar()">Buscar</button>
<button onclick="limpiar()">Borrar</button>

<div id="res"></div>

<script>
function icono(r){
    if(!r) return "";
    r=r.toLowerCase();
    if(r.includes("solo")) return "🟢";
    if(r.includes("validacion")) return "⚠️";
    if(r.includes("autorizacion")) return "🔒";
    return "";
}

function buscar(){
    fetch('/api/academicos?q='+encodeURIComponent(q.value))
    .then(r=>r.json())
    .then(d=>{
        if(!d.length){ res.innerHTML="Sin resultados"; return; }

        let h="<table><tr><th>Académico</th><th>Cargo</th><th>Contacto</th></tr>";
        d.forEach(r=>{
            h+=`<tr>
<td>
<span class="info">ℹ️ ${r.nombre}
<span class="tooltip">
📧 <a href="mailto:${r.correo_director}" style="color:#8fd">${r.correo_director||"—"}</a><br>
👩‍💼 ${r.secretaria_nombre||"—"}<br>
📧 <a href="mailto:${r.secretaria_correo}" style="color:#8fd">${r.secretaria_correo||"—"}</a><br>
${icono(r.consultar_antes_de_entregar_contactos)} ${r.consultar_antes_de_entregar_contactos||""}
</span>
</span>
</td>
<td>${r.cargo||""}</td>
<td>${r.sede||""}</td>
</tr>`;
        });
        h+="</table>";
        res.innerHTML=h;
    });
}

function limpiar(){
    q.value="";
    res.innerHTML="";
}
</script>

</div>
</body>
</html>
"""

# =========================
# EJECUCIÓN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


