from flask import Flask, request
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
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Directorio UMAYOR</title>
        <style>
            body { font-family: Arial; margin: 40px; }
            input { width: 300px; padding: 8px; }
            button { padding: 8px 12px; }
            .card { border: 1px solid #ccc; padding: 15px; margin: 10px 0; }
            .titulo { font-weight: bold; font-size: 18px; }
        </style>
    </head>
    <body>

    <h1>Directorio UMAYOR</h1>

    <form method="get" action="/buscar">
        <input type="text" name="q" placeholder="Escribe medicina, vet, tem...">
        <button type="submit">Buscar</button>
    </form>

    </body>
    </html>
    """

# 🔍 Buscador con resultados bonitos
@app.route("/buscar")
def buscar():
    q = request.args.get("q", "").lower()

    if len(q) < 3:
        return "<p>Escribe al menos 3 letras.</p>"

    data = supabase.table("directorio_umayor") \
        .select("*") \
        .or_(f"nombre.ilike.%{q}%,escuela.ilike.%{q}%,cargo.ilike.%{q}%") \
        .execute()

    resultados = ""

    for p in data.data:
        resultados += f"""
        <div class="card">
            <div class="titulo">{p.get('nombre','')}</div>
            <p><b>Escuela:</b> {p.get('escuela','')}</p>
            <p><b>Cargo:</b> {p.get('cargo','')}</p>
            <p><b>Campus:</b> {p.get('campus','')}</p>
            <p><b>Facultad:</b> {p.get('facultad','')}</p>
            <p><b>Director:</b> {p.get('correo director','')}</p>
            <p><b>Secretaria:</b> {p.get('secretaria','')}</p>
            <p><b>Correo secretaria:</b> {p.get('correo secretaria','')}</p>
            <p><b>Sede:</b> {p.get('sede','')}</p>
        </div>
        """

    return f"""
    <html>
    <body>
        <a href="/">← Volver</a>
        <h2>Resultados para: {q}</h2>
        {resultados}
    </body>
    </html>
    """

# ▶️ Ejecutar
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
