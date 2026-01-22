from flask import Flask, request, jsonify
from supabase import create_client

app = Flask(__name__)

SUPABASE_URL = "https://wkbltctqqsuxqhlbnoeg.supabase.co"
SUPABASE_KEY = "sb_publishable_vpm9GsG9AbVjH80qxfzIfQ_RuFq8uAd"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def normalizar(texto):
    if not texto:
        return ""
    texto = texto.lower()
    texto = texto.replace(" ", "")
    texto = texto.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n")
    texto = texto.replace(".","").replace("'","")
    return texto

campus_links = {
    "huechuraba": "https://www.umayor.cl/um/santiago-campus-huechuraba",
    "santodomingo": "https://www.umayor.cl/um/santiago-campus-santo-domingo",
    "elclaustro": "https://www.umayor.cl/um/santiago-campus-el-claustro",
    "alameda": "https://www.umayor.cl/um/santiago-campus-alameda",
    "estadiomayor": "https://www.umayor.cl/um/santiago-campus-estadio-mayor",
    "conservatorio": "https://www.umayor.cl/um/santiago-campus-conservatorio",
    "alemania": "https://www.umayor.cl/um/santiago-campus-alemania-temuco"
}

@app.route("/")
def home():
    return """
    <h1>Directorio Escuelas UMAYOR</h1>

    <input id="busqueda" placeholder="Ej: administracion publica, medicina, derecho">

    <select id="sede">
        <option value="">Todas</option>
        <option value="santiago">Santiago</option>
        <option value="temuco">Temuco</option>
    </select>

    <button onclick="buscar()">Buscar</button>

    <br><br>

    <table border="1" cellpadding="6">
        <thead>
            <tr>
                <th>Director</th>
                <th>Correo Director</th>
                <th>Secretaria</th>
                <th>Correo Secretaria</th>
                <th>Anexo</th>
                <th>Campus</th>
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
                    <td>${d["correo director"] || ""}</td>
                    <td>${d.secretaria || ""}</td>
                    <td>${d["correo secretaria"] || ""}</td>
                    <td>${d["anexo secretaria"] || ""}</td>
                    <td>${d.campus_link || ""}</td>
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

@app.route("/buscar")
def buscar():
    q = request.args.get("q", "")
    sede = request.args.get("sede", "")

    q_limpio = normalizar(q)

    if len(q_limpio) < 3:
        return jsonify([])

    data = supabase.table("directorio_umayor").select("*").execute().data

    resultados = []

    for d in data:
        texto = normalizar(f"{d.get('escuela','')}")

        if q_limpio in texto:
            if sede:
                if normalizar(d.get("sede","")) != normalizar(sede):
                    continue

            campus_raw = normalizar(d.get("campus",""))
            link = campus_links.get(campus_raw, "")
            d["campus_link"] = f'<a href="{link}" target="_blank">{d.get("campus","")}</a>' if link else d.get("campus","")

            resultados.append(d)

    return jsonify(resultados)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


