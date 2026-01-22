from flask import Flask, request, jsonify
from supabase import create_client
import unicodedata

app = Flask(__name__)

# 🔑 Supabase
SUPABASE_URL = "https://wkbltctqqsuxqhlbnoeg.supabase.co"
SUPABASE_KEY = "sb_publishable_vpm9GsG9AbVjH80qxfzIfQ_RuFq8uAd"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🔤 Normalizar texto (quitar acentos, espacios, mayúsculas)
def limpiar(texto):
    if not texto:
        return ""
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = texto.replace(" ", "")
    return texto

# 🏠 Página principal
@app.route("/")
def home():
    return """
    <html>
    <head>
        <style>
            body {
                font-family: Calibri, Arial, sans-serif;
                padding: 20px;
            }
            input, select, button {
                font-size: 16px;
                padding: 5px;
                margin-right: 5px;
            }
            table {
                border-collapse: collapse;
                margin-top: 20px;
                width: 100%;
            }
            th, td {
                border: 1px solid #ccc;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    <body>

        <h1>Directorio UMAYOR</h1>

        <input id="busqueda" placeholder="Ej: medicina, vet, admi">
        
        <select id="sede">
            <option value="">Todas</option>
            <option value="Santiago">Santiago</option>
            <option value="Temuco">Temuco</option>
        </select>

        <button onclick="buscar()">Buscar</button>
        <button onclick="limpiar()">Borrar</button>

        <div id="tabla"></div>

        <script>
        function buscar() {
            const q = document.getElementById("busqueda").value;
            const sede = document.getElementById("sede").value;

            fetch(`/buscar?q=${q}&sede=${sede}`)
                .then(r => r.json())
                .then(data => {
                    if (data.length === 0) {
                        document.getElementById("tabla").innerHTML = "<p>No se encontraron resultados.</p>";
                        return;
                    }

                    let html = "<table><tr>";
                    html += "<th>Nombre</th><th>Escuela</th><th>Cargo</th><th>Campus</th>";
                    html += "<th>Correo Director</th><th>Secretaria</th>";
                    html += "<th>Correo Secretaria</th><th>Sede</th><th>Restricción</th></tr>";

                    data.forEach(r => {
                        html += `<tr>
                            <td>${r.nombre || ""}</td>
                            <td>${r.escuela || ""}</td>
                            <td>${r.cargo || ""}</td>
                            <td>${r.Campus || ""}</td>
                            <td>${r["correo director"] || ""}</td>
                            <td>${r.secretaria || ""}</td>
                            <td>${r["correo secretaria"] || ""}</td>
                            <td>${r.sede || ""}</td>
                            <td>${r["consultar antes de entregar contactos"] || ""}</td>
                        </tr>`;
                    });

                    html += "</table>";
                    document.getElementById("tabla").innerHTML = html;
                });
        }

        function limpiar() {
            document.getElementById("busqueda").value = "";
            document.getElementById("sede").value = "";
            document.getElementById("tabla").innerHTML = "";
        }
        </script>

    </body>
    </html>
    """

# 🔍 Buscador
@app.route("/buscar")
def buscar():
    q = limpiar(request.args.get("q", ""))
    sede = request.args.get("sede", "")

    if len(q) < 3:
        return jsonify([])

    query = supabase.table("directorio_escuelas").select("*")

    if sede:
        query = query.eq("sede", sede)

    data = query.execute().data

    resultados = []

    for r in data:
        texto = limpiar(
            (r.get("nombre","") +
             r.get("escuela","") +
             r.get("cargo",""))
        )

        if q in texto:
            resultados.append(r)

    return jsonify(resultados)

# ▶️ Ejecutar
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


