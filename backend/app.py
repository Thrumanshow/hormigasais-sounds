from flask import Flask, jsonify, send_from_directory, abort, request
import json
import os
from datetime import datetime

app = Flask(__name__)

# Ruta a archivos premium
PREMIUM_DIR = "backend/premium_files"

# Cargar lista de sonidos/images premium desde JSON
with open(os.path.join("backend", "sounds.json")) as f:
    premium_list = json.load(f)

@app.route("/premium/list")
def list_premium():
    """Devuelve todos los archivos Premium disponibles"""
    return jsonify(premium_list)

@app.route("/premium/download/<premium_id>")
def download_premium(premium_id):
    """Simula autorización y entrega de archivo Premium"""
    # Buscar en la lista
    file_info = next((item for item in premium_list if item["premium_id"] == premium_id), None)
    if not file_info:
        return abort(404, description="Archivo no encontrado o no autorizado")
    
    # Aquí podrías agregar validación de usuario LBH/M2M si quieres
    filename = os.path.basename(file_info["download_url"])
    return send_from_directory(PREMIUM_DIR, filename, as_attachment=True)

@app.route("/premium/upload", methods=["POST"])
def upload_premium():
    """Simula subir un archivo Premium"""
    if "file" not in request.files:
        return abort(400, description="No se subió ningún archivo")
    
    file = request.files["file"]
    premium_id = f"HS-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    filename = f"{premium_id}_{file.filename}"
    save_path = os.path.join(PREMIUM_DIR, filename)
    file.save(save_path)

    # Generar JSON de metadata
    new_entry = {
        "premium_id": premium_id,
        "original_filename": file.filename,
        "uploaded_by": "demo_user",
        "timestamp": datetime.utcnow().isoformat(),
        "hash": "dummyhash1234567890",  # Puedes calcular hash real si quieres
        "file_type": file.content_type,
        "size_bytes": os.path.getsize(save_path),
        "premium_level": "gold",
        "LBH_signature": "dummyLBHsig987654321",
        "download_url": f"premium_files/{filename}"
    }

    # Guardar en lista
    premium_list.append(new_entry)
    with open(os.path.join("backend", "sounds.json"), "w") as f:
        json.dump(premium_list, f, indent=2)

    return jsonify(new_entry), 201

if __name__ == "__main__":
    app.run(debug=True, port=5000)
