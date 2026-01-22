from flask import Flask, request, render_template_string
from supabase import create_client

app = Flask(__name__)

# 🔑 Credenciales Supabase
SUPABASE_URL = "https://wkbltctqqsuxqhlbnoeg.supabase.co"
SUPABASE_KEY = "sb_publishable_vpm9GsG9AbVjH80qxfzIfQ_RuFq8uAd"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Directorio UMAYOR</title>
    <style>
        body { font-family: Arial; }
        input, select, button { padding: 8px; margin: 5px; }
        table { border-collapse: collapse; width: 100%; margin-top: 15px; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>

<h1>Directorio UMAYOR</h1>

<form method="get" action="/buscar">
    <input name="q" placeholder="Escribe: medicina, vet, derecho..." required>
    
    <select name="sede">
        <option value="">Todas</option>
        <option value="santiago">Santiago</option>
        <option value="temuco">Temuco</option>
    </select>

    <button type="submit">Buscar</button>
</form>

{% if resultados %}
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
    </tr>

    {% for r in resultados %}
    <tr>
        <td>{{ r.nombre }}</td>
        <td>{{ r.escuela }}</td>
        <td>{{ r.cargo }}</td>
        <td>{{ r.campus }}</td>
        <td>{{ r.correo_director }}</td>
        <td>{{ r.secretaria }}</td>
        <td>{{ r.correo_secretaria }}</td>
        <td>{{ r.sede }}</td>
        <td>{{ r.consultar_antes_de_entregar_contactos }}</td>
    </tr>
    {% endfor %}
</table>
{% endif %}

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/buscar")
def buscar():
    q = request.args.get("q", "").lower()
    sede = request.args.get("sede", "").lower()

    if len(q) < 3:
        return render_template_string(HTML, resultados=[])

    query = supabase.table("directorio_escuelas").select(
        "nombre, escuela, cargo, campus, correo_director, secretaria, correo_secretaria, sede, consultar_antes_de_entregar_contactos"
    ).or_(
        f"nombre.ilike.%{q}%,escuela.ilike.%{q}%,cargo.ilike.%{q}%"
    )

    if sede:
        query = query.ilike("sede", f"%{sede}%")

    data = query.execute().data

    return render_template_string(HTML, resultados=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


