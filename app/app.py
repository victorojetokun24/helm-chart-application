import os
from datetime import datetime, timezone
import psycopg
from flask import Flask, jsonify
app = Flask(__name__)
VERSION = os.getenv("APP_VERSION", "4.0.0")
DB_HOST = os.getenv("DB_HOST", "swiftcart-dev-swiftcart-postgres")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("POSTGRES_DB", "swiftcart")
DB_USER = os.getenv("POSTGRES_USER", "swiftcart")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "swiftcartpass")
def conn():
    return psycopg.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, connect_timeout=3)
@app.get("/")
def home():
    with conn() as c:
        with c.cursor() as q:
            q.execute("CREATE TABLE IF NOT EXISTS visits (id SERIAL PRIMARY KEY, visited_at TIMESTAMPTZ NOT NULL DEFAULT NOW())")
            q.execute("INSERT INTO visits DEFAULT VALUES")
            q.execute("SELECT COUNT(*) FROM visits")
            visits = q.fetchone()[0]
            c.commit()
    return f"<h1>SwiftCart Logistics</h1><p>Running on Kubernetes with Helm</p><p>Version: {VERSION}</p><p>Database: {DB_HOST}:{DB_PORT}</p><p>Visits: {visits}</p>"
@app.get("/health")
def health():
    return jsonify(status="healthy", service="swiftcart-api", version=VERSION)
@app.get("/api/db-check")
def db_check():
    with conn() as c:
        with c.cursor() as q:
            q.execute("SELECT version()")
            version = q.fetchone()[0]
    return jsonify(database="postgresql", connected=True, server_version=version)
@app.get("/api/status")
def status():
    with conn() as c:
        with c.cursor() as q:
            q.execute("SELECT COUNT(*) FROM visits")
            visits = q.fetchone()[0]
    return jsonify(application="SwiftCart Logistics", status="running", orchestrated_by="Kubernetes + Helm", version=VERSION, database_host=DB_HOST, visits=visits, timestamp=datetime.now(timezone.utc).isoformat())
