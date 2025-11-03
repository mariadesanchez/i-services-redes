from flask import Flask, request, jsonify
from instagrapi import Client
import json
import os
from datetime import datetime
from pydantic import HttpUrl
from uuid import UUID

app = Flask(__name__)

SESSION_FILE = "session.json"


# ✅ Función auxiliar para convertir cualquier objeto raro a string
def safe_json(data, status=200):
    def default(o):
        if isinstance(o, (HttpUrl, UUID, datetime)):
            return str(o)
        return str(o)
    return app.response_class(
        response=json.dumps(data, ensure_ascii=False, default=default),
        status=status,
        mimetype='application/json'
    )


@app.route('/')
def home():
    return safe_json({"message": "Instagram microservice running", "status": "ok"})


# 📦 Subir una sesión ya validada
@app.route('/session', methods=['POST'])
def upload_session():
    try:
        data = request.get_json()
        if not data:
            return safe_json({"error": "Missing JSON body"}, 400)

        with open(SESSION_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        return safe_json({"message": "Session file saved successfully"})
    except Exception as e:
        return safe_json({"error": str(e)}, 500)


# 👥 Obtener followers usando sesión guardada
@app.route('/followers', methods=['GET', 'POST'])
def get_followers():
    try:
        if not os.path.exists(SESSION_FILE):
            return safe_json({"error": "Session not found. Upload it via /session first."}, 400)

        data = request.get_json(force=True, silent=True) or {}
        username = data.get("username")

        cl = Client()
        cl.load_settings(SESSION_FILE)

        if not username:
            username = cl.username

        user_id = cl.user_id_from_username(username)
        followers = cl.user_followers(user_id)

        def user_to_dict(u):
            return {
                "pk": u.pk,
                "username": u.username,
                "full_name": u.full_name,
                "profile_pic_url": str(u.profile_pic_url),
                "is_private": u.is_private,
            }

        followers_list = [user_to_dict(u) for u in followers.values()]
        return safe_json({"followers": followers_list, "count": len(followers_list)})

    except Exception as e:
        return safe_json({"error": str(e)}, 500)


# 👥 Obtener following usando sesión guardada
@app.route('/following', methods=['GET', 'POST'])
def get_following():
    try:
        if not os.path.exists(SESSION_FILE):
            return safe_json({"error": "Session not found. Upload it via /session first."}, 400)

        data = request.get_json(force=True, silent=True) or {}
        username = data.get("username")

        cl = Client()
        cl.load_settings(SESSION_FILE)

        if not username:
            username = cl.username

        user_id = cl.user_id_from_username(username)
        following = cl.user_following(user_id)

        def user_to_dict(u):
            return {
                "pk": u.pk,
                "username": u.username,
                "full_name": u.full_name,
                "profile_pic_url": str(u.profile_pic_url),
                "is_private": u.is_private,
            }

        following_list = [user_to_dict(u) for u in following.values()]
        return safe_json({"following": following_list, "count": len(following_list)})

    except Exception as e:
        return safe_json({"error": str(e)}, 500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
