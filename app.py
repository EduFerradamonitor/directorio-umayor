from flask import Flask, request, jsonify
from supabase import create_client

app = Flask(__name__)

SUPABASE_URL = "https://wkbltctqqsuxqhlbnoeg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndrYmx0Y3RxcXN1eHFobGJub2VnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjkwMDI1NzYsImV4cCI6MjA4NDU3ODU3Nn0.QLl8XI79jOC_31RjtTMCwrKAXNg-Y1Bt_x2JQL9rnEM"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Directorio UMAYOR</title>
        <style>
            body {
                font-family: Calibri, Arial, sans-serif;
                background: #f3f6f9;
            }
            .card {
                max-width: 900px;
                margin: 50px auto;
                background: white;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 0 20px rgba(0,0,0,0.1);
            }
            input, select, button {
                width: 100%;
                padding: 12px;
                margin: 10px 0;
                font-size: 16px;
            }
            button {
                background: #005baa;
                color: white;
                border: none;
                cursor: pointer;
            }
            button.secondary {
                background: #999;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
                font-size: 14px;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            th {
                background: #005baa;
                color: white;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>📘 Directorio UMAYOR</h1>

            <input id="busqueda" placeholder="Ingrese escuela aqui">

            <select id="sede">
                <option value="">Todas las sedes</option>
                <option value="Santiago">Santiago</option>
                <option value="Temuco">Temuco</option>
            </select>

            <button onclick="buscar()">Buscar</button>
            <button class="secondary" onclick="borrar()">Borrar</button>

            <div id="resultados"></div>
        </div>

        <script>
        function buscar() {
            const q = document.getElementById("busqueda").value;
            const sede = document.getElementById("sede").value;

            fetch(`/buscar?q=${q}&sede=${sede}`)
            .then(r => r.json())
            .then(data => {
                if (data.length === 0) {
                    document.getElementById("resultados").innerHTML =
                        "<p>No se encontraron resultados.</p>";
                    return;
                }

                let html = "<table><tr>" +
                    "<th>Nombre</th><th>Escuela</th><th>Cargo</th><th>Campus</th>" +
                    "<th>Correo Director</th><th>Secretaria</th><th>Correo Secretaria</th>" +
                    "<th>Sede</th><th>Restricción</th></tr>";

                data.forEach(r => {
                    html += `<tr>
                        <td>${r.nombre || ""}</td>
                        <td>${r.escuela_busqueda || ""}</td>
                        <td>${r.cargo || ""}</td>
                        <td>${r.Campus || ""}</td>
                        <td>${r.correo_director || ""}</td>
                        <td>${r.secretaria || ""}</td>
                        <td>${r.correo_secretaria || ""}</td>
                        <td>${r.sede || ""}</td>
                        <td>${r.consultar_antes_de_entregar_contactos || ""}</td>
                    </tr>`;
                });

                html += "</table>";
                document.getElementById("resultados").innerHTML = html;
            });
        }

        function borrar() {
            document.getElementById("busqueda").value = "";
            document.getElementById("sede").value = "";
            document.getElementById("resultados").innerHTML = "";
        }
        </script>
    </body>
    </html>
    """

@app.route("/buscar")
def buscar():
    q = request.args.get("q", "").strip().lower()
    sede = request.args.get("sede", "").strip()

    if len(q) < 2:
        return jsonify([])

    query = supabase.table("directorio_escuelas").select("*") \
        .or_(f"""
            nombre.ilike.%{q}%,
            escuela.ilike.%{q}%,
            escuela_busqueda.ilike.%{q}%,
            cargo.ilike.%{q}%
        """)

    if sede:
        query = query.eq("sede", sede)

    data = query.execute().data
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)






