from flask import Flask, request, jsonify, url_for
from supabase import create_client

app = Flask(__name__)

# =========================
# CONFIGURACIÓN SUPABASE
# =========================
SUPABASE_URL = "https://wkbltctqqsuxqhlbnoeg.supabase.co"
SUPABASE_KEY = "sb_publishable_vpm9GsG9AbVjH80qxfzIfQ_RuFq8uAd"
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
    align-items: center;
    justify-content: space-between;
    margin-bottom: 25px;
}}

.logo-um {{
    height: 120px;
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
    margin-top: 20px;
}}

table {{
    width: 100%;
    min-width: 1100px;
    border-collapse: collapse;
}}

th, td {{
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
    vertical-align: top;
    white-space: nowrap;
}}

th {{
    background: #005baa;
    color: white;
}}

td.wrap {{
    white-space: normal;
    max-width: 260px;
}}

.restr-ok {{ color: green; font-weight: bold; }}
.restr-warn {{ color: orange; font-weight: bold; }}
.restr-lock {{ color: #c96f00; font-weight: bold; }}

.tooltip {{
    position: relative;
    display: inline-block;
    cursor: pointer;
}}

.tooltip .tooltiptext {{
    visibility: hidden;
    width: 230px;
    background-color: #333;
    color: #fff;
    text-align: left;
    padding: 8px;
    border-radius: 6px;
    position: absolute;
    z-index: 10;
    bottom: 125%;
    left: 50%;
    transform: translateX(-50%);
    font-size: 13px;
}}

.tooltip:hover .tooltiptext {{
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
        <img src="{url_for('static', filename='img/logoum.jpg')}" class="logo-um" alt="Universidad Mayor">
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

<script>
function restriccionHTML(texto) {{
    if (!texto) return "";
    texto = texto.toLowerCase();
    if (texto.includes("solo correo")) return "<span class='restr-ok'>🟢 Solo correo secretaría</span>";
    if (texto.includes("validacion")) return "<span class='restr-warn'>⚠️ Validación previa</span>";
    if (texto.includes("autorizacion")) return "<span class='restr-lock'>🔒 Autorización expresa</span>";
    return texto;
}}

function tooltipAnexos(r) {{
    const ad = r.anexo_director || "Sin información";
    const as = r.anexo_secretaria || "Sin información";
    return `
    <span class="tooltip">📞
        <span class="tooltiptext">
            <strong>Anexo director:</strong> ${'{'}ad{'}'}<br>
            <strong>Anexo secretaría:</strong> ${'{'}as{'}'}
        </span>
    </span>`;
}}

function buscar() {{
    const q = document.getElementById("busqueda").value;
    const sede = document.getElementById("sede").value;

    fetch(`/buscar?q=${'{'}encodeURIComponent(q){'}'}&sede=${'{'}encodeURIComponent(sede){'}'}`)
    .then(r => r.json())
    .then(data => {{
        if (!data || data.length === 0) {{
            document.getElementById("resultados").innerHTML =
                "<p>No se encontraron resultados.</p>";
            return;
        }}

        let html = `<div class="table-wrapper"><table>
        <tr>
            <th>Nombre</th>
            <th>Escuela</th>
            <th>Cargo</th>
            <th>Campus</th>
            <th>Correo Director</th>
            <th>Secretaría</th>
            <th>Correo Secretaría</th>
            <th>Sede</th>
            <th>Restricción</th>
        </tr>`;

        data.forEach(r => {{
            html += `<tr>
                <td>${'{'}r.nombre || ""{'}'}</td>
                <td class="wrap">${'{'}r.escuela_busqueda || r.escuela || ""{'}'}</td>
                <td class="wrap">${'{'}r.cargo || ""{'}'}</td>
                <td>${'{'}r.campus || ""{'}'}</td>
                <td>${'{'}r.correo_director || ""{'}'} ${'{'}tooltipAnexos(r){'}'}</td>
                <td>${'{'}r.secretaria || ""{'}'}</td>
                <td>${'{'}r.correo_secretaria || ""{'}'}</td>
                <td>${'{'}r.sede || ""{'}'}</td>
                <td>${'{'}restriccionHTML(r.consultar_antes_de_entregar_contactos){'}'}</td>
            </tr>`;
        }});

        html += "</table></div>";
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
    return jsonify(result.data or [])

# =========================
# EJECUCIÓN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



