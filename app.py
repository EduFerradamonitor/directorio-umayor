from flask import Flask, request, jsonify
from supabase import create_client
import os
import unicodedata
import re

app = Flask(__name__)

SUPABASE_URL = "https://wkbltctqqsuxqhlbnoeg.supabase.co"
SUPABASE_KEY = "sb_publishable_vpm9GsG9AbVjH80qxfzIfQ_RuFq8uAd"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🔤 Limpieza de texto (quita tildes, espacios, símbolos)
def normalizar(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    texto = re.sub(r'[^a-z0-9]', '', texto)
    return texto

@app.route("/")
def home():
    return """
    <html>
    <head>
        <style>
            body { font-family: Calibri, Arial, sans-serif; padding: 40px; }
            input, select, button { font-size: 16px; padding: 6px; }
            table { border-collapse: collapse; margin-top: 20px; width: 100%; }
            th, td { border: 1px solid #ccc; padding: 8px; }
            th { background: #f2f2f2; }
        </style>
    </head>
    <body>

    <h1>Directorio UMAYOR</h1>

    <input id="busqueda" placeholder="Ej: odontologia, inge, admin...">
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
                document.getElementById("resultado").innerHTML = "No se encontraron resultados.";
                return;
            }

            let tabla = `
            <table>
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
            </tr>`;

            data.forEach(d => {
                tabla += `
                <tr>
                    <td>${d.nombre || ""}</td>
                    <td>${d.escuela || ""}</td>
                    <td>${d.cargo || ""}</td>
                    <td>${d.Campus || ""}</td>
                    <td>${d["correo director"] || ""}</td>
                    <td>${d.secretaria || ""}</td>
                    <td>${d["correo secretaria"] || ""}</td>
                    <td>${d.sede || ""}</td>
                    <td>${d["consultar antes de entregar contactos"] || ""}</td>
                </tr>`;
            });

            tabla += "</table>";
            document.getElementById("resultado").innerHTML = tabla;
        });
    }

    function borrar() {
        document.getElementById("busqueda").value = "";
        document.getElementById("resultado").innerHTML = "";
    }
    </script>

    </body>
    </html>
    """

@app.route("/buscar")
def buscar():
    q = request.args.get("q", "")
    sede = request.args.get("sede", "")

    q_limpio = normalizar(q)

    query = supabase.table("directorio_escuelas").select("*")

    if q_limpio:
        query = query.or_(
            f"nombre.ilike.%{q}%,"
            f"escuela.ilike.%{q}%,"
            f"cargo.ilike.%{q}%"
        )

    if sede:
        query = query.eq("sede", sede)

    data = query.execute().data

    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



