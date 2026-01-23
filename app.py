from flask import Flask

app = Flask(__name__)

# =========================
# CARÁTULA PRINCIPAL
# =========================
@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Directorio Institucional UM</title>

<style>
body {
    font-family: Calibri, Arial, sans-serif;
    background: #f3f6f9;
    margin: 0;
}

.header {
    background: #ffffff;
    border-bottom: 4px solid #f5c842;
    padding: 20px 40px;
    display: flex;
    align-items: center;
}

.header img {
    height: 80px; /* LOGO MÁS PROTAGÓNICO */
}

.container {
    max-width: 1100px;
    margin: 40px auto;
    padding: 20px;
}

h1 {
    font-size: 32px;
    margin-bottom: 6px;
}

.subtitle {
    color: #555;
    margin-bottom: 40px;
    font-size: 16px;
}

.cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 25px;
    margin-bottom: 40px;
}

.card {
    background: white;
    border-radius: 12px;
    padding: 25px;
    box-shadow: 0 0 15px rgba(0,0,0,0.08);
    text-decoration: none;
    color: black;
    transition: transform 0.2s;
}

.card:hover {
    transform: translateY(-4px);
}

.card h2 {
    margin-top: 0;
    color: #005baa;
}

.links {
    background: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 0 15px rgba(0,0,0,0.08);
}

.links strong {
    font-size: 16px;
}

.links select {
    width: 100%;
    padding: 12px;
    font-size: 15px;
    margin-top: 10px;
}

.footer {
    margin-top: 60px;
    text-align: center;
    font-size: 13px;
    color: #555;
}
</style>
</head>

<body>

<div class="header">
    <img src="/static/img/logoum.jpg" alt="Universidad Mayor">
</div>

<div class="container">
    <h1>Directorio Institucional UM</h1>
    <div class="subtitle">
        Accesos centralizados para atención y gestión académica
    </div>

    <div class="cards">
        <a class="card" href="/escuelas">
            <h2>📘 Directorio de Escuelas</h2>
            <p>
                Información de directores y secretarías de escuelas.
            </p>
        </a>

        <a class="card" href="/academicos">
            <h2>📗 Otros Contactos Académicos</h2>
            <p>
                Coordinaciones, núcleos académicos y apoyos institucionales.
            </p>
        </a>
    </div>

    <div class="links">
        <strong>🔗 Links de interés</strong>
        <select onchange="if(this.value) window.open(this.value, '_blank')">
            <option value="">Selecciona un enlace…</option>
            <option value="https://www.umayor.cl/um/servicios-estudiantiles/Registro-Estudiantes">
                ORE – Registro de Estudiantes
            </option>
            <option value="https://sso.umayor.cl/authentication/SignIn?SID=13&app_url=certificadosalumnos.umayor.cl">
                Portal de Certificados
            </option>
            <option value="https://www.umayor.cl/um/servicios-estudiantiles/Gratuidad-Becas-y-ayudas-estudiantiles">
                Becas y Créditos
            </option>
            <option value="https://www.umayor.cl/um/servicios-estudiantiles/Gestion-Financiera">
                Gestión Financiera
            </option>
            <option value="https://www.umayor.cl/um/oferta-academica">
                Oferta Académica
            </option>
            <option value="https://www.admisionmayor.cl/preguntas-frecuentes">
                Preguntas Frecuentes Admisión
            </option>
        </select>
    </div>

    <div class="footer">
        Desarrollado por <strong>Eduardo Ferrada</strong><br>
        Universidad Mayor · Enero 2026
    </div>
</div>

</body>
</html>
"""

# =========================
# PLACEHOLDERS (NO TOCAR)
# =========================
@app.route("/escuelas")
def escuelas():
    return "<h2>Directorio de Escuelas UM</h2><p>Módulo existente</p>"

@app.route("/academicos")
def academicos():
    return "<h2>Otros Contactos Académicos</h2><p>Módulo en construcción</p>"

# =========================
# EJECUCIÓN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



