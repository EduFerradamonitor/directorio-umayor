from flask import Flask, request, jsonify, render_template_string
from supabase import create_client
import unicodedata
import re

app = Flask(__name__)

# 🔑 Supabase
SUPABASE_URL = "https://wkbltctqqsuxqhlbnoeg.supabase.co"
SUPABASE_KEY = "sb_publishable_vpm9GsG9AbVjH80qxfzIfQ_RuFq8uAd"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🧼 Limpieza de texto
def limpiar(texto):
    if not texto:
        return ""
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = re.sub(r"[\u0300-\u036f]", "", texto)
    texto = re.sub(r"[^a-z0-9]", "", texto)
    return texto

# 🏠 Interfaz principal
@app.route("/")
def home():
    return render_template_string("""
    <html>
    <head>
        <style>
            body { font-family: Calibri, Arial, sans-serif; margin: 40px; }
            input, select, button { padding: 8px; font-size: 16px; }
            table { border-collapse: collapse; width: 100%; margin-top: 20px; }
            th, td { border: 1px solid #ccc; padding: 8px; }
            th { background: #f2f2f2; }
        </style>
    </head>
    <body>
        <h1>Directorio UMAYOR</h1>

        <input id="busqueda" placeholder="Ej: medicina, inge, vet..." style="width:300px;">
        
        <select id="sede">
            <option value="">Todas</option>
            <option value="Santiago">Santiago</option>
            <option value="Temuco">Temuco</option>
        </select>

        <button onclick="buscar()">Buscar</button>
        <button onclick="borrar()">Borrar</button>

        <div id="resultado"></div>

        <script>
        function buscar() {
            const q = document.getElementById("busqueda").value;
            const sede = document.getElementById("sede").value;

            fetch(`/buscar?q=${q}&sede=${sede}`)
            .then(r => r.json())
            .then(data => {
                if (data.length === 0) {
                    document.getElementById("resultado").innerHTML = 
                        "<p>No se encontraron resultados.</p>";
                    return;
                }

                let html = "<table><tr>";
                const columnas = [
                    "nombre","escuela","cargo","Campus",
                    "correo director","secretaria",
                    "correo secretaria","sede",
                    "consultar antes de entregar contactos"
                ];

                columnas.forEach(c => html += `<th>${c}</th>`);
                html += "</tr>";

                data.forEach(r => {
                    html += "<tr>";
                    columnas.forEach(c => {
                        html += `<td>${r[c] || ""}</td>`;
                    });
                    html += "</tr>";
                });

                html += "</table>";
                document.getElementById("resultado").innerHTML = html;
            });
        }

        function borrar() {
            document.getElementById("busqueda").value = "";
            document.getElementById("sede").value = "";
            document.getElementById("resultado").innerHTML = "";
        }
        </script>
    </body>
    </html>
    """)

# 🔍 Buscador inteligente
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
             r.get("cargo","") +
             r.get("Campus",""))
        )

        # Búsqueda por fragmentos
        fragmentos = [q[i:i+3] for i in range(len(q)-2)]

        if any(f in texto for f in fragmentos):
            resultados.append(r)

    return jsonify(resultados)

# ▶️ Ejecutar
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



