from flask import Flask, jsonify
import os
import psycopg2
from psycopg2 import OperationalError

app = Flask(__name__)

@app.get("/health")
def health():
    # Récupération des variables d'environnement (avec valeurs par défaut)
    db_host = os.environ.get("DB_HOST", "db")
    db_port = os.environ.get("DB_PORT", "5432")
    db_user = os.environ.get("POSTGRES_USER", "campus")
    db_password = os.environ.get("POSTGRES_PASSWORD", "dev-password")
    db_name = os.environ.get("POSTGRES_DB", "campus")

    try:
        # Tentative de connexion à la base de données
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            dbname=db_name,
            connect_timeout=3
        )
        conn.close()
        db_status = "connected"
    except OperationalError as e:
        db_status = f"disconnected"
        # Si la DB n'est pas joignable, on renvoie une erreur 503 (Service Unavailable)
        return jsonify(status="error", db_status=db_status, details=str(e)), 503

    return jsonify(status="ok", db_status=db_status)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
