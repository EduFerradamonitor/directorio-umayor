from flask import Flask, request, jsonify
from supabase import create_client

app = Flask(__name__)

SUPABASE_URL = "https://wkbltctqqsuxqhlbnoeg.supabase.co"
SUPABASE_KEY = "sb_publishable_vpm9GsG9AbVjH80qxfzIfQ_RuFq8uAd"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/")
def home():
    return """
    <h1>Directorio UMAYOR</h1>

    <input id="busqueda" placeholder="Ej: medicina, veterinaria..." style="width:300px;">
    
    <select id="sede">
        <option value="">Todas</option>
        <option value="Santiago">Santiago</option>
        <option value="Temuco">Temuco</option>
    </select>

    <button onclick="buscar()">Buscar</button>

    <div id="resultado"></div>

    <script>
    function buscar() {
        const q = document.getElementById("busqueda").value;
        const sede = document.getElementById("sede").value;

        fetch(`/buscar?q=${q}&sede=${sede}`)
        .then(r => r.json())
        .then(data => {
            let html = "<table border='1'><tr><th>Nombre</th><th>Escuela</th><th>Cargo</th><th>Campus</th><th>Correo Director</th><th>Secretaria</th><th>Correo Secretaria</th><th>Sede</th><th>Restricción</th></tr>";

            data.forEach(p => {
                html += `<tr>
                    <td>${p.nombre || ""}</td>
                    <td>${p.escuela || ""}</td>
                    <td>${p.cargo || ""}</td>
                    <td>${p.Campus || ""}</td>
                    <td>${p["correo director"] || ""}</td>
                    <td>${p.secretaria || ""}</td>
                    <td>${p["correo secretaria"] || ""}</td>
                    <td>${p.sede || ""}</td>
                    <td>${p["consultar antes de entregar contactos"] || ""}</td>
                </tr>`;
            });

            html += "</table>";
            document.getElementById("resultado").innerHTML = html;
        });
    }
    </script>
    """

@app.route("/buscar")
def buscar():
    q = request.args.get("q", "").lower()
    sede = request.args.get("sede", "")

    if len(q) < 3:
        return jsonify([])

    query = supabase.table("directorio_escuelas") \
        .select("*") \
        .or_(f"nombre.ilike.%{q}%,escuela.ilike.%{q}%,cargo.ilike.%{q}%")

    if sede:
        query = query.eq("sede", sede)

    data = query.execute().data
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

