from flask import Flask, render_template, request, jsonify
from supabase import create_client

app = Flask(__name__)

# =========================
# CONFIGURACIÓN SUPABASE
# =========================
SUPABASE_URL = "https://wkbltctqqsuxqhlbnoeg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndrYmx0Y3RxcXN1eHFobGJub2VnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjkwMDI1NzYsImV4cCI6MjA4NDU3ODU3Nn0.QLl8XI79jOC_31RjtTMCwrKAXNg-Y1Bt_x2JQL9rnEM"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# =========================
# HOME
# =========================
@app.route("/")
def home():
    return render_template("home.html")

# =========================
# ESCUELAS (NO SE TOCA)
# =========================
@app.route("/escuelas")
def escuelas():
    return render_template("escuelas.html")

@app.route("/api/escuelas")
def api_escuelas():
    q = request.args.get("q", "").strip().lower()
    sede = request.args.get("sede", "").strip().lower()

    if len(q) < 2:
        return jsonify([])

    query = (
        supabase
        .table("directorio_escuelas_umayor")
        .select("""
            nombre,
            cargo,
            correo_director,
            secretaria,
            correo_secretaria,
            escuela_busqueda,
            sede,
            campus,
            anexo_director,
            anexo_secretaria,
            consultar_antes_de_entregar_contactos
        """)
        .or_(
            f"nombre.ilike.%{q}%,"
            f"cargo.ilike.%{q}%,"
            f"escuela_busqueda.ilike.%{q}%"
        )
    )

    if sede:
        query = query.ilike("sede", sede)

    result = query.execute()
    return jsonify(result.data or [])

# =========================
# ACADÉMICOS (DESDE CERO, LIMPIO)
# =========================
@app.route("/academicos")
def academicos():
    return render_template("academicos.html")

@app.route("/api/academicos")
def api_academicos():
    q = request.args.get("q", "").strip().lower()

    if len(q) < 2:
        return jsonify([])

    query = (
        supabase
        .table("otros_contactos_academicos")
        .select("""
            nombre,
            cargo,
            departamento,
            correo_director,
            secretaria_nombre,
            secretaria_correo,
            anexo_director,
            anexo_secretaria,
            consultar_antes_de_entregar_contactos,
            sede
        """)
        .ilike("departamento_busqueda", f"%{q}%")
    )

    result = query.execute()
    return jsonify(result.data or [])

# =========================
# EJECUCIÓN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)




