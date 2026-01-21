
from flask import Flask, request, jsonify
from supabase import create_client
import os

app = Flask(__name__)

# 🔑 Tus datos de Supabase
SUPABASE_URL = "https://wkbltctqqsuxqhlbnoeg.supabase.co"
SUPABASE_KEY = "sb_publishable_vpm9GsG9AbVjH80qxfzIfQ_RuFq8uAd"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🏠 Ruta principal
@app.route("/")
def home():
    return """
    <h1>Directorio UMAYOR</h1>
    <input id="busqueda" placeholder="Escribe medicina, vet, tem..." style="width:300px;">
    <button onclick="buscar()">Buscar</button>
    <pre id="resultado"></pre>

    <script>
    function buscar() {
        const q = document.getElementById("busqueda").value;
        fetch("/buscar?q=" + q)
        .then(r => r.json())
        .then(data => {
            document.getElementById("resultado").textContent = JSON.stringify(data, null, 2);
        });
    }
    </script>
    """

# 🔍 Buscador inteligente
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
