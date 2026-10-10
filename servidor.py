from flask import Flask, request, jsonify
import sqlite3, time, os

app = Flask(__name__)
DB = "datos.db"

def init():
    c = sqlite3.connect(DB)
    c.execute("""CREATE TABLE IF NOT EXISTS servidores(
        job TEXT PRIMARY KEY, huevo TEXT, tamano REAL, valor REAL,
        rareza TEXT, jugadores INTEGER, ts REAL)""")
    c.commit(); c.close()
init()

@app.route("/reportar", methods=["POST"])
def reportar():
    d = request.get_json(force=True)
    c = sqlite3.connect(DB)
    c.execute("""INSERT INTO servidores(job,huevo,tamano,valor,rareza,jugadores,ts)
        VALUES(?,?,?,?,?,?,?)
        ON CONFLICT(job) DO UPDATE SET
        huevo=excluded.huevo, tamano=excluded.tamano, valor=excluded.valor,
        rareza=excluded.rareza, jugadores=excluded.jugadores, ts=excluded.ts""",
        (d.get("job"), d.get("huevo",""), d.get("tamano",0), d.get("valor",0),
         d.get("rareza",""), d.get("jugadores",0), time.time()))
    c.commit(); c.close()
    return jsonify(ok=True)

@app.route("/servidores")
def servidores():
    limite = time.time() - 60
    c = sqlite3.connect(DB)
    filas = c.execute("SELECT * FROM servidores WHERE ts > ? ORDER BY tamano DESC", (limite,)).fetchall()
    c.close()
    cols = ["job","huevo","tamano","valor","rareza","jugadores","ts"]
    return jsonify([dict(zip(cols,f)) for f in filas])

@app.route("/")
def home():
    return "Sensor Steal An Egg activo"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))
