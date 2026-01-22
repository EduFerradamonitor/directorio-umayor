from flask import Flask, request, jsonify
from supabase import create_client

app = Flask(__name__)

# 🔑 Datos Supabase
SUPABASE_URL = "https://wkbltctqqsuxqhlbnoeg.supabase.co"
SUPABASE_KEY = "sb_publishable_vpm9GsG9AbVjH80qxfzIfQ_RuFq8uAd"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🏠 Página principal
@app.route("/")
def home():
    return """
    <html>
    <head>
        <style>
            body {
                font-family: Calibri, Arial, sans-serif;
                background: #f4f6f8;
                padding: 30px;
            }
            .box {
                background: white;
                padding: 20px;
                border-radius: 10px;
                max-width: 900px;
                margin: auto;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            input, select, button {
                padding: 10px;
                margin: 5px 0;
                width: 100%;
                font-size: 16px;
            }
            button {
                background: #005baa;
                color: white;
                border: none;
                cursor: pointer;
            }
            button:hover {
                background: #004080;
            }
            .resultado {
                margin-top: 20px;
                white-space: pre-wrap;
                font-size: 14px;
                background: #eef2f5;
                padding: 15px;
                border-radius: 8px;
            }
        </style>
    </head>
    <body>
        <div class="box">
            <h2>📘 Directorio UMAYOR</h2>

            <input id="busqueda" placeholder="Ej: medicina, veter, fono, admi...">

            <select id="sede">
                <option value="">Todas las sedes</option>
                <option value="Santiago">Santiago</option>
                <option value="Temuco">Temuco</option>
            </select>

            <button onclick="buscar()">Buscar</button>
            <button onclick="limpiar()" style="background:#999;">Borrar</button>

            <div id="resultado" class="resultado"></div>
        </div>

        <script>
        function buscar() {
            const q = document.getElementById("busqueda").value;
            const sede = document.getElementById("sede").value;

            fetch(`/buscar?q=${q}&sede=${sede}`)
            .then(r => r.json())
            .then(data => {
                if (data.length === 0) {
                    document.getElementById("resultado").textContent = "No se encontraron resultados.";
                    return;
                }

                let texto = "";
                data.forEach(d => {
                    texto += 
`Nombre: ${d.nombre}
Escuela: ${d.escuela}
Cargo: ${d.cargo}
Campus: ${d.campus}
Correo Director: ${d.correo_director}
Secretaria: ${d.secretaria}
Correo Secretaria: ${d.correo_secretaria}
Sede: ${d.sede}
Restricción: ${d.consultar_antes_de_entregar_contactos}
-----------------------------\n`;
                });

                document.getElementById("resultado").textContent = texto;
            });
        }

        function limpiar() {
            document.getElementById("busqueda").value = "";
            document.getElementById("sede").value = "";
            document.getElementById("resultado").textContent = "";
        }
        </script>
    </body>
    </html>
    """

# 🔍 Buscador
@app.route("/buscar")
def buscar():
    q = request.args.get("q", "").lower()
    sede = request.args.get("sede", "")

    if len(q) < 3:
        return jsonify([])

    query = supabase.table("directorio_escuelas") \
        .select("nombre, escuela, cargo, campus, correo_director, secretaria, correo_secretaria, sede, consultar_antes_de_entregar_contactos") \
    .or_(f"nombre.ilike.%{q}%,escuela.ilike.%{q}%,escuela_busqueda.ilike.%{q}%,cargo.ilike.%{q}%")

    if sede:
        query = query.eq("sede", sede)

    data = query.execute().data
    return jsonify(data)

# ▶️ Ejecutar
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)






