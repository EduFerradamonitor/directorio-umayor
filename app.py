from flask import Flask, request, jsonify, url_for
from supabase import create_client

app = Flask(__name__)

# =========================
# CONFIGURACIÓN SUPABASE
# =========================
SUPABASE_URL = "https://wkbltctqqsuxqhlbnoeg.supabase.co"
SUPABASE_KEY = "TU_PUBLIC_KEY_AQUI"  # deja la tuya real

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# =========================
# PÁGINA PRINCIPAL
# =========================
@app.route("/")
def home():
    logo_url = url_for("static", filename="img/logoum.jpg")

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
    box-shadow: 0 0 22px rgba(0,0,0,0.12);
}}

.header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
}}

.logo-um {{
    height: 100px;
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
    margin-top: 25px;
    overflow-x: auto;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    min-width: 1100px;
}}

th, td {{
    border: 1px solid #ddd;
    padding: 8px;
    vertical-align: top;
}}

th {{
    background: #005baa;
    color: white;
    text-align: left;
}}

th.sede, td.sede {{
    width: 90px;
    text-align: center;
    white-space: nowrap;
}}

.copy {{
    cursor: pointer;
    color: #005baa;
}}

.copy:hover {{
    text-decoration: underline;
}}

.tooltip {{
    position: relative;
    cursor: help;
}}

.tooltip .tooltiptext {{
    visibility: hidden;
    width: 220px;
    background-color: #333;
    color: #fff;
    text-align: left;
    padding: 8px;
    border-radius: 6px;
    position: absolute;
    z-index: 10;
    top: -5px;
    left: 105%;
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
        <img src="{logo_url}" class="logo-um" alt="Universidad Mayor">
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
function copiar(texto) {{
    navigator.clipboard.writeText(texto);
    alert("Copiado al portapapeles");
}}

function iconoRestriccion(texto) {{
    if (!texto) return "🟠 Información sensible";

    texto = texto.toLowerCase();

    if (texto.includes("solo correo")) return "🟢 Solo correo secretaría";
    if (texto.includes("validacion")) return "⚠️ Validación previa";
    if (texto.includes("autorizacion")) return "🔒 Autorización expresa";

    return "🟠 Información sensible";
}}

function respuestaSugerida(texto) {{
    if (!texto) return "Estimado/a, para este contacto se recomienda validar antes de entregar información.";

    texto = texto.toLowerCase();

    if (texto.includes("solo correo"))
        return "Estimado/a, para este caso solo corresponde entregar el correo de la secretaría.";

    if (texto.includes("validacion"))
        return "Estimado/a, este contacto requiere validación previa antes de entregar información.";

    if (texto.includes("autorizacion"))
        return "Estimado/a, este contacto requiere autorización expresa antes de entregar información.";

    return "Estimado/a, este contacto tiene restricciones. Favor validar antes de entregar datos.";
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

        let html = `<div class="table-wrapper"><table>
        <tr>
            <th>Nombre</th>
            <th>Escuela</th>
            <th>Cargo</th>
            <th>Campus</th>
            <th>Correo Director</th>
            <th>Secretaría</th>
            <th>Correo Secretaría</th>
            <th class="sede">Sede</th>
            <th>Restricción</th>
            <th>Respuesta</th>
        </tr>`;

        data.forEach(r => {{
            const anexoDir = r.anexo_director || "Sin información";
            const anexoSec = r.anexo_secretaria || "Sin información";

            html += `<tr>
                <td>${{r.nombre || ""}}</td>
                <td>${{r.escuela_busqueda || r.escuela || ""}}</td>
                <td>${{r.cargo || ""}}</td>
                <td>${{r.campus || ""}}</td>
                <td>
                    <span class="copy" onclick="copiar('${{r.correo_director || ""}}')">
                        ${{r.correo_director || "no informado"}}
                    </span>
                    <div class="tooltip">📞
                        <span class="tooltiptext">Anexo director: ${{anexoDir}}</span>
                    </div>
                </td>
                <td>${{r.secretaria || ""}}</td>
                <td>
                    <span class="copy" onclick="copiar('${{r.correo_secretaria || ""}}')">
                        ${{r.correo_secretaria || "no informado"}}
                    </span>
                    <div class="tooltip">📞
                        <span class="tooltiptext">Anexo secretaría: ${{anexoSec}}</span>
                    </div>
                </td>
                <td class="sede">${{r.sede || ""}}</td>
                <td>${{iconoRestriccion(r.consultar_antes_de_entregar_contactos)}}</td>
                <td>
                    <span class="copy" onclick="copiar(respuestaSugerida('${{r.consultar_antes_de_entregar_contactos || ""}}'))">
                        📝 Copiar
                    </span>
                </td>
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
# BUSCADOR
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

