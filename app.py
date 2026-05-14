from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import torch
import torch.nn as nn
from torchvision import models, transforms
from ultralytics import YOLO
from PIL import Image
import io
import base64
import torch.nn.functional as F
import sqlite3
import os
import uuid
import datetime
import json

app = FastAPI()

# Mount static files for images
os.makedirs("static/uploads", exist_ok=True)
os.makedirs("static/results", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# ------------------ DB Setup ------------------
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scans (
            id TEXT PRIMARY KEY,
            patient_id TEXT,
            patient_name TEXT,
            patient_age INTEGER,
            patient_gender TEXT,
            scan_date TEXT,
            modality TEXT,
            inference_result TEXT,
            severity TEXT,
            status TEXT,
            original_path TEXT,
            annotated_path TEXT,
            predictions TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ------------------ Load Models ------------------
device = torch.device("cpu")

# YOLO
yolo_model = YOLO("best.pt")

# Classification
model = models.resnet50(weights=None)
model.fc = nn.Sequential(
    nn.Linear(model.fc.in_features, 256),
    nn.ReLU(),
    nn.Dropout(0.5),
    nn.Linear(256, 14)
)

model.load_state_dict(torch.load("model.pth", map_location=device))
model.eval()

# Transform
transform = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor()
])

classes = [
"Aortic enlargement","Atelectasis","Calcification","Cardiomegaly",
"Consolidation","ILD","Infiltration","Lung Opacity",
"Nodule/Mass","Other lesion","Pleural effusion",
"Pleural thickening","Pneumothorax","Pulmonary fibrosis"
]

# ------------------ Routes ------------------

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html") as f:
        return f.read()

@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    patient_id: str = Form(...),
    patient_name: str = Form(...),
    patient_age: str = Form(...),
    patient_gender: str = Form(...)
):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    # Generate unique ID
    scan_id = str(uuid.uuid4())
    
    # Save original image to disk
    orig_path = f"static/uploads/{scan_id}.png"
    image.save(orig_path, format="PNG")

    # Convert original image to base64 for immediate display
    orig_buffer = io.BytesIO()
    image.save(orig_buffer, format="PNG")
    original_str = base64.b64encode(orig_buffer.getvalue()).decode()

    # YOLO
    results = yolo_model(image)
    annotated = results[0].plot()

    # Save annotated image to disk
    annot_path = f"static/results/{scan_id}.png"
    img = Image.fromarray(annotated)
    img.save(annot_path, format="PNG")

    # Convert annotated image to base64 for immediate display
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    annotated_str = base64.b64encode(buffer.getvalue()).decode()

    # YOLO predictions extraction (take max conf per class)
    yolo_preds = {}
    if hasattr(results[0], 'boxes') and results[0].boxes is not None:
        for box in results[0].boxes:
            cls_id = int(box.cls[0].item())
            conf = float(box.conf[0].item()) * 100
            label = results[0].names[cls_id]
            if label not in yolo_preds or conf > yolo_preds[label]:
                yolo_preds[label] = conf

    # Classification
    img_tensor = transform(image).unsqueeze(0)
    output = model(img_tensor)
    probs = F.softmax(output, dim=1)

    # Get top 3 predictions from ResNet
    top_probs, top_indices = torch.topk(probs, 3, dim=1)
    resnet_predictions = {
        classes[top_indices[0][i].item()]: float(top_probs[0][i].item()) * 100
        for i in range(3)
    }
    
    # Merge YOLO and ResNet predictions (take max confidence)
    combined_dict = {}
    for k, v in resnet_predictions.items():
        combined_dict[k] = v
    for k, v in yolo_preds.items():
        if k in combined_dict:
            combined_dict[k] = max(combined_dict[k], v)
        else:
            combined_dict[k] = v
            
    # Sort by confidence descending and take top 3
    sorted_preds = sorted(combined_dict.items(), key=lambda x: x[1], reverse=True)
    top_predictions = [{"class": k, "confidence": v} for k, v in sorted_preds[:3]]
    
    # If no predictions (edge case), default to No Findings
    if not top_predictions:
        top_predictions = [{"class": "No Findings", "confidence": 0.0}]
        
    primary_class = top_predictions[0]["class"]
    primary_conf = top_predictions[0]["confidence"]
    
    if primary_class == "No Findings" and primary_conf >= 50:
        severity = "Normal (02%)"
        status = "Verified by AI"
    elif primary_class == "No Findings" and primary_conf < 50:
        severity = "Inconclusive"
        status = "Pending Review"
    elif primary_conf > 50:
        if primary_conf >= 90:
            severity = f"Critical ({int(primary_conf)}%)"
        else:
            severity = f"Moderate ({int(primary_conf)}%)"
        status = "Pending Review"
    else:
        severity = f"Inconclusive ({int(primary_conf)}%)"
        status = "Pending Review"

    # Save to DB
    scan_date = datetime.datetime.now().strftime("%b %d, %Y")
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO scans (id, patient_id, patient_name, patient_age, patient_gender, scan_date, modality, inference_result, severity, status, original_path, annotated_path, predictions)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (scan_id, patient_id, patient_name, patient_age, patient_gender, scan_date, "DX Chest PA", primary_class, severity, status, orig_path, annot_path, json.dumps(top_predictions)))
    conn.commit()
    conn.close()

    return {
        "id": scan_id,
        "patient_id": patient_id,
        "patient_name": patient_name,
        "patient_age": patient_age,
        "patient_gender": patient_gender,
        "original_image": f"data:image/png;base64,{original_str}",
        "annotated_image": f"data:image/png;base64,{annotated_str}",
        "top_predictions": top_predictions
    }

@app.get("/api/scans")
def get_scans():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT id, patient_id, scan_date, modality, inference_result, severity, status FROM scans ORDER BY rowid DESC')
    rows = c.fetchall()
    conn.close()
    
    scans = []
    for r in rows:
        scans.append({
            "id": r[0],
            "patient_id": r[1],
            "scan_date": r[2],
            "modality": r[3],
            "inference_result": r[4],
            "severity": r[5],
            "status": r[6]
        })
    return {"scans": scans}

@app.get("/api/scans/{scan_id}")
def get_scan(scan_id: str):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM scans WHERE id = ?', (scan_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0],
            "patient_id": row[1],
            "patient_name": row[2],
            "patient_age": row[3],
            "patient_gender": row[4],
            "scan_date": row[5],
            "modality": row[6],
            "inference_result": row[7],
            "severity": row[8],
            "status": row[9],
            "original_path": "/" + row[10],
            "annotated_path": "/" + row[11],
            "predictions": json.loads(row[12])
        }
    return JSONResponse(status_code=404, content={"message": "Scan not found"})