@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Directorio UMAYOR</title>

<style>
body {
    font-family: Calibri, Arial, sans-serif;
    background: #f3f6f9;
}

.card {
    max-width: 1100px;
    margin: 40px auto;
    background: white;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 0 20px rgba(0,0,0,0.1);
}

.header {
    display: flex;
    align-items: center;
    gap: 20px;
}

.header img {
    width: 130px;
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

.table-wrapper {
    overflow-x: auto;
    margin-top: 20px;
}

table {
    width: 100%;
    border-collapse: collapse;
}

th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
    vertical-align: top;
    word-break: break-word;
}

th {
    background: #005baa;
    color: white;
}

/* Anchos por columna */
th:nth-child(1), td:nth-child(1) { min-width: 180px; }
th:nth-child(2), td:nth-child(2) { min-width: 160px; }
th:nth-child(3), td:nth-child(3) { min-width: 160px; }
th:nth-child(4), td:nth-child(4) { min-width: 180px; }
th:nth-child(5), td:nth-child(5) { min-width: 220px; }
th:nth-child(6), td:nth-child(6) { min-width: 160px; }
th:nth-child(7), td:nth-child(7) { min-width: 220px; }
th:nth-child(8), td:nth-child(8) { min-width: 100px; }
th:nth-child(9), td:nth-child(9) { min-width: 160px; }

.badge {
    font-weight: bold;
}

.verde { color: #2e7d32; }
.naranja { color: #f57c00; }
.rojo { color: #c62828; }
.gris { color: #777; }
</style>
</head>

<body>
<div class="card">

<div class="header">
    <img src="https://raw.githubusercontent.com/EduFerradamonitor/directorio-umayor/main/logoum.jpg">
    <h1>Directorio UMAYOR</h1>
</div>

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
</body>
</html>
"""



