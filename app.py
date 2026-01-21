from flask import Flask, request, jsonify
from supabase import create_client

app = Flask(__name__)

# 🔑 Credenciales Supabase
SUPABASE_URL = "https://wkbltctqqsuxqhlbnoeg.supabase.co"
SUPABASE_KEY = "sb_publishable_vpm9GsG9AbVjH80qxfzIfQ_RuFq8uAd"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🏠 Página principal
@app.route("/")
def home():
    return """
    <h1>Directorio UMAYOR</h1>

    <input id="busqueda" placeholder="Escribe medicina, vet, tem..." style="width:300px;">

    <select id="sede">
        <option value="">Todas las sedes</option>
        <option value="Santiago">Santiago</option>
        <option value="Temuco">Temuco</option>
    </select>

    <button onclick="buscar()">Buscar</button>

    <br><br>

    <table border="1" cellpadding="6">
        <thead>
            <tr>
                <th>Nombre</th>
                <th>Escuela</th>
                <th>Cargo</th>
                <th>Campus</th>
                <th>Correo Director</th>
                <th>Secretaria</th>
                <th>Correo Secretaria</th>
                <th>Sede</th>
                <th>Restricción</th>
            </tr>
        </thead>
        <tbody id="tabla"></tbody>
    </table>

    <script>
    function buscar() {
        const q = document.getElementById("busqueda").value;
        const sede = document.getElementById("sede").value;

        fetch(`/buscar?q=${q}&sede=${sede}`)
        .then(r => r.json())
        .then(data => {
            const tabla = document.getElementById("tabla");
            tabla.innerHTML = "";

            data.forEach(d => {
                const fila = `
                <tr>
                    <td>${d.nombre || ""}</td>
                    <td>${d.escuela || ""}</td>
                    <td>${d.cargo || ""}</td>
                    <td>${d.campus || ""}</td>
                    <td>${d["correo director"] || ""}</td>
                    <td>${d.secretaria || ""}</td>
                    <td>${d["correo secretaria"] || ""}</td>
                    <td>${d.sede || ""}</td>
                    <td>${d["consultar antes de entregar contactos"] || ""}</td>
                </tr>
                `;
                tabla.innerHTML += fila;
            });
        });
    }
    </script>
    """

# 🔍 Buscador con filtro por sede
@app.route("/buscar")
def buscar():
    q = request.args.get("q", "").lower()
    sede = request.args.get("sede", "")

    if len(q) < 3:
        return jsonify([])

    query = supabase.table("directorio_umayor") \
        .select("*") \
        .or_(f"nombre.ilike.%{q}%,escuela.ilike.%{q}%,cargo.ilike.%{q}%")

    if sede:
        query = query.eq("sede", sede)

    data = query.execute()

    return jsonify(data.data)

# ▶️ Ejecutar
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)




