import os
import json
from instagrapi import Client, exceptions
from flask import Flask, jsonify

app = Flask(__name__)

# Nombre del archivo local de sesión
SESSION_FILE = "session.json"

# 🧠 1. Crear session.json desde variable de entorno si no existe
if not os.path.exists(SESSION_FILE):
    session_data = os.getenv("SESSION_JSON")
    if session_data:
        try:
            with open(SESSION_FILE, "w", encoding="utf-8") as f:
                f.write(session_data)
            print("✅ session.json creado desde variable de entorno.")
        except Exception as e:
            print("❌ Error al crear session.json:", e)
    else:
        print("⚠️ No se encontró la variable de entorno SESSION_JSON. Es necesario para autenticar.")
        exit(1)

# 🪄 2. Inicializar cliente de Instagram
cl = Client()

try:
    cl.load_settings(SESSION_FILE)
    cl.get_timeline_feed()  # test rápido para confirmar sesión válida
    print("✅ Sesión cargada y válida.")
except exceptions.LoginRequired:
    print("⚠️ La sesión no es válida. Ejecutá session.py localmente para generar una nueva session.json.")
    exit(1)
except Exception as e:
    print("❌ Error al cargar sesión:", e)
    exit(1)

# 📦 3. Ejemplo de endpoint Flask
@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "Instagram API funcionando correctamente ✅"})

# 👤 4. Endpoint para mostrar info del usuario autenticado
@app.route("/me")
def me():
    try:
        user_info = cl.account_info()
        return jsonify({
            "username": user_info.username,
            "full_name": user_info.full_name,
            "pk": user_info.pk,
            "is_private": user_info.is_private,
            "profile_pic_url": user_info.profile_pic_url
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🚀 5. Arrancar el servidor Flask
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
