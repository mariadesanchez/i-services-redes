# import os
import json
import os
from flask import Flask, jsonify
from instagrapi import Client, exceptions

app = Flask(__name__)

SESSION_FILE = "session.json"

# 🧠 Crear session.json desde variable de entorno si no existe
if not os.path.exists(SESSION_FILE):
    session_data = os.getenv("SESSION_JSON")
    if session_data:
        try:
            with open(SESSION_FILE, "w", encoding="utf-8") as f:
                f.write(session_data)
            print("✅ session.json creado desde variable de entorno.")
        except Exception as e:
            print("❌ Error al crear session.json:", e)
            exit(1)
    else:
        print("⚠️ No se encontró la variable de entorno SESSION_JSON.")
        exit(1)

# 🪄 Inicializar cliente de Instagram
cl = Client()

try:
    cl.load_settings(SESSION_FILE)
    cl.get_timeline_feed()  # test rápido
    print("✅ Sesión cargada y válida.")
except exceptions.LoginRequired:
    print("⚠️ La sesión no es válida. Genera una nueva con session.py.")
    exit(1)
except Exception as e:
    print("❌ Error al cargar sesión:", e)
    exit(1)

# 👥 Lista de seguidores (followers)
@app.route("/followers")
def followers():
    try:
        user_id = cl.user_id
        followers = cl.user_followers(user_id)

        result = [
            {
                "username": getattr(f, "username", None),
                "full_name": getattr(f, "full_name", None),
                "pk": getattr(f, "pk", None),
                "is_private": bool(getattr(f, "is_private", False)),
                "profile_pic_url": getattr(f, "profile_pic_url", None),
            }
            for f in followers.values()
        ]

        return jsonify(result)

    except Exception as e:
        print("❌ Error en /followers:", e)
        return jsonify({"error": str(e)}), 500


# ➕ Lista de seguidos (following)
@app.route("/following")
def following():
    try:
        user_id = cl.user_id
        following = cl.user_following(user_id)

        result = [
            {
                "username": getattr(f, "username", None),
                "full_name": getattr(f, "full_name", None),
                "pk": getattr(f, "pk", None),
                "is_private": bool(getattr(f, "is_private", False)),
                "profile_pic_url": getattr(f, "profile_pic_url", None),
            }
            for f in following.values()
        ]

        return jsonify(result)

    except Exception as e:
        print("❌ Error en /following:", e)
        return jsonify({"error": str(e)}), 500


# 🚀 Servidor Flask
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
