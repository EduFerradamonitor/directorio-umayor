from flask import Flask, request, jsonify
from supabase import create_client

app = Flask(__name__)

# 🔑 Datos de Supabase
SUPABASE_URL = "https://wkbltctqqsuxqhlbnoeg.supabase.co"
SUPABASE_KEY = "sb_publishable_vpm9GsG9AbVjH80qxfzIfQ_RuFq8uAd"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🏠 Página principal
@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>Directorio UMAYOR</title>
        <style>
            body { font-family: Arial; padding: 20px; }
            input { width: 300px; padding: 6px; }
            button { padding: 6px 10px; }
            table { border-collapse: collapse; width: 100%; margin-top: 20px; }
            th, td { border: 1px solid #ccc; padding: 6px; text-align: left; }
            th { background: #f2f2f2; }
        </style>
    </head>
    <body>
        <h1>Directorio UMAYOR</h1>

        <input id="busqueda" placeholder="Escribe medicina, vet, tem...">
        <button onclick="buscar()">Buscar</button>

        <div id="resultado"></div>

        <script>
        function buscar() {
            const q = document.getElementById("busqueda").value;

            fetch("/buscar?q=" + q)
            .then(r => r.json())
            .then(data => {
                let html = "";

                if (data.length === 0) {
                    html = "<p>No se encontraron resultados.</p>";
                } else {
                    html = "<table><tr>" +
                        "<th>Nombre</th>" +
                        "<th>Escuela</th>" +
                        "<th>Cargo</th>" +
                        "<th>Campus</th>" +
                        "<th>Facultad</th>" +
                        "<th>Correo Director</th>" +
                        "<th>Secretaria</th>" +
                        "<th>Correo Secretaria</th>" +
                        "</tr>";

                    data.forEach(d => {
                        html += "<tr>" +
                            "<td>" + (d.nombre || "") + "</td>" +
                            "<td>" + (d.escuela || "") + "</td>" +
                            "<td>" + (d.cargo || "") + "</td>" +
                            "<td>" + (d.campus || "") + "</td>" +
                            "<td>" + (d.facultad || "") + "</td>" +
                            "<td>" + (d["correo director"] || "") + "</td>" +
                            "<td>" + (d.secretaria || "") + "</td>" +
                            "<td>" + (d["correo secretaria"] || "") + "</td>" +
                        "</tr>";
                    });

                    html += "</table>";
                }

                document.getElementById("resultado").innerHTML = html;
            });
        }
        </script>
    </body>
    </html>
    """

# 🔍 Buscador
@app.route("/buscar")
def buscar():
    q = request.args.get("q", "").lower()

    if len(q) < 3:
        return jsonify([])

    data = supabase.table("directorio_umayor") \
        .select("*") \
        .or_(f"nombre.ilike.%{q}%,escuela.ilike.%{q}%,cargo.ilike.%{q}%") \
        .execute()

    return jsonify(data.data)

# ▶️ Ejecutar
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


