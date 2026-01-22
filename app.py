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
                max-width: 850px;
                margin: 40px auto;
                background: white;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 0 20px rgba(0,0,0,0.1);
            }
            .logo {
                text-align: center;
                margin-bottom: 15px;
            }
            .logo img {
                max-width: 180px;
            }
            h1 {
                text-align: center;
                margin-bottom: 25px;
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
            .restriccion {
                font-weight: bold;
            }
            .verde { color: #2e7d32; }
            .naranja { color: #f57c00; }
            .rojo { color: #c62828; }
        </style>
    </head>
    <body>
        <div class="card">

            <div class="logo">
                <img src="/static/img/logum.jpg" alt="Universidad Mayor">
            </div>

            <h1>📘 Directorio UMAYOR</h1>

            <input id="busqueda" placeholder="¿Qué escuela busca? (ej: vet, derecho, psicología)">

            <select id="sede">
                <option value="">Todas las sedes</option>
                <option value="santiago">Santiago</option>
                <option value="temuco">Temuco</option>
            </select>

            <button onclick="buscar()">Buscar</button>
            <button class="secondary" onclick="borrar()">Borrar</button>

            <div id="resultados"></div>
        </div>

        <script>
        function iconoRestriccion(texto) {
            if (!texto) return "<span class='restriccion naranja'>🟠 Sin información</span>";

            texto = texto.toLowerCase();

            if (texto.includes("solo correo")) {
                return "<span class='restriccion verde'>🟢 Solo correo secretaría</span>";
            }
            if (texto.includes("validacion")) {
                return "<span class='restriccion naranja'>🟠 Con validación previa</span>";
            }
            if (texto.includes("autorizacion")) {
                return "<span class='restriccion rojo'>🔴 Autorización expresa</span>";
            }

            return "<span class='restriccion naranja'>🟠 " + texto + "</span>";
        }

        function buscar() {
            const q = document.getElementById("busqueda").value;
            const sede = document.getElementById("sede").value;

            fetch(`/buscar?q=${encodeURIComponent(q)}&sede=${encodeURIComponent(sede)}`)
            .then(r => r.json())
            .then(data => {
                if (!data || data.length === 0) {
                    document.getElementById("resultados").innerHTML = "<p>No se encontraron resultados.</p>";
                    return;
                }

                let html = "<table><tr>" +
                    "<th>Nombre</th><th>Escuela</th><th>Cargo</th><th>Campus</th>" +
                    "<th>Correo Director</th><th>Secretaría</th><th>Correo Secretaría</th>" +
                    "<th>Sede</th><th>Restricción</th></tr>";

                data.forEach(r => {
                    html += `<tr>
                        <td>${r.nombre || ""}</td>
                        <td>${r.escuela_busqueda || r.escuela || ""}</td>
                        <td>${r.cargo || ""}</td>
                        <td>${r.campus || ""}</td>
                        <td>${r.correo_director || ""}</td>
                        <td>${r.secretaria || ""}</td>
                        <td>${r.correo_secretaria || ""}</td>
                        <td>${r.sede || ""}</td>
                        <td>${iconoRestriccion(r.consultar_antes_de_entregar_contactos)}</td>
                    </tr>`;
                });

                html += "</table>";
                document.getElementById("resultados").innerHTML = html;
            })
            .catch(err => {
                document.getElementById("resultados").innerHTML = "<p>Error al consultar los datos.</p>";
                console.error(err);
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

# 🔍 Buscador con filtros correctos
@app.route("/buscar")
def buscar():
    q = request.args.get("q", "").strip().lower()
    sede = request.args.get("sede", "").strip().lower()

    if len(q) < 2:
        return jsonify([])

    query = (
        supabase
        .table("directorio_escuelas")
        .select("*")
        .or_(
            f"escuela_busqueda.ilike.%{q}%,"
            f"escuela.ilike.%{q}%,"
            f"nombre.ilike.%{q}%,"
            f"cargo.ilike.%{q}%"
        )
    )

    if sede:
        query = query.ilike("sede", f"%{sede}%")

    result = query.execute()

    return jsonify(result.data if result.data else [])

# ▶️ Ejecutar
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)







