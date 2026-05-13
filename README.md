
---

# 🫁 CliniScan AI

### End-to-End Medical AI System for Lung Abnormality Detection in Chest X-Rays

![Python](https://img.shields.io/badge/Python-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-red)
![FastAPI](https://img.shields.io/badge/FastAPI-green)
![Docker](https://img.shields.io/badge/Docker-blue)
![YOLOv8](https://img.shields.io/badge/YOLOv8-black)
![HuggingFace](https://img.shields.io/badge/Deployed-HuggingFace-yellow)
![Status](https://img.shields.io/badge/Status-Production_Ready-brightgreen)

---

## 🧠 Overview

CliniScan AI is a **full-stack, production-grade medical AI system** designed to detect, classify, and localize lung abnormalities in chest X-ray (CXR) images.

It integrates:

* 🧠 Deep Learning (CNN models like EfficientNet / ResNet)
* 📦 Object Detection (YOLOv8)
* 🔍 Explainable AI (Grad-CAM)
* ⚙️ FastAPI backend
* 🎨 Frontend (HTML, CSS, JavaScript)
* 🐳 Dockerized deployment
* 🌐 Hugging Face hosting

---

## 🖥️ Interface Preview

### 🏠 Home Page

![Home Page](output/home.jpeg)


### 📊 Model Output

![Output](output/output.jpeg)

---

## 🎯 Objective

To assist radiologists by building an AI system that:

* Detects lung diseases from X-rays
* Localizes abnormal regions
* Provides visual explanations
* Improves diagnostic speed and accuracy

---

## 🚀 Key Features

✔ Multi-label lung disease detection <br>
✔ YOLOv8-based abnormality localization <br>
✔ CNN-based classification (EfficientNet / ResNet) <br>
✔ Grad-CAM explainability <br>
✔ FastAPI real-time inference API <br>
✔ Docker containerized deployment <br>
✔ Interactive web UI (frontend integration) <br>
✔ Hugging Face hosted demo <br>

---
### 🏗️ System Architecture

![Architecture](output/system_arrchitecture.jpeg)

---

## 📊 Dataset

**VinDr-CXR Dataset**

* 18,000+ labeled chest X-rays
* Bounding box annotations
* Multi-disease classification

🔗 [https://physionet.org/content/vindr-cxr/1.0.0/](https://physionet.org/content/vindr-cxr/1.0.0/)

---

## 🧠 AI Models

| Component      | Model                 |
| -------------- | --------------------- |
| Classification | EfficientNet / ResNet |
| Detection      | YOLOv8                |
| Explainability | Grad-CAM              |

---

## ⚙️ Tech Stack

### Data Processing

* pydicom
* OpenCV
* NumPy
* Pandas

### AI / ML

* PyTorch
* YOLOv8
* EfficientNet
* ResNet

### Backend

* FastAPI
* Uvicorn

### Frontend

* React
* HTML
* CSS
* JavaScript

### Deployment

* Docker
* Hugging Face Spaces

---

## 🌐 Live Demo

👉 [[CliniScan AI](https://huggingface.co/spaces/shubhamsalunke/CliniScan-Pro)]

---

## 📈 Performance

| Model        | Task           | Metric  | Score |
| ------------ | -------------- | ------- | ----- |
| EfficientNet | Classification | AUC     | 0.88  |
| YOLOv8       | Detection      | mAP@0.5 | 0.75  |

---

## 🧪 Workflow

1. Upload Chest X-ray
2. Preprocessing (DICOM handling)
3. AI inference
4. Disease classification + detection
5. Grad-CAM visualization
6. API response
7. UI display

---

## 🐳 Run Locally

```bash
git clone https://github.com/your-username/CliniScanAI-Lung-Abnormality-Detection.git
cd CliniScanAI-Lung-Abnormality-Detection

pip install -r requirements.txt
```

### ▶ Start Backend

```bash
uvicorn deployment.backend.main:app --reload
```

### ▶ Open Frontend

```bash
open output/home.jpeg
```

---

## 🐳 Docker Run

```bash
docker build -t clinscan-ai .
docker run -p 8000:8000 clinscan-ai
```

---

## 📌 Project Highlights

✔ Real-world medical AI system <br>
✔ Full-stack deployment (Frontend + Backend + ML) <br>
✔ Production-ready FastAPI service <br>
✔ Explainable AI (Grad-CAM) <br>
✔ Containerized using Docker <br>
✔ Deployed on Hugging Face <br>
✔ Clinical dataset (VinDr-CXR) <br>

---

## 🏆 Milestones

### 🟢 Milestone 1

Data pipeline + preprocessing

### 🟡 Milestone 2

Baseline ML models

### 🟠 Milestone 3

Optimization + Grad-CAM

### 🔵 Milestone 4

Deployment + full-stack integration

---

## 🤝 Contribution

1. Fork repo
2. Create feature branch
3. Submit PR

---

## 📜 License

MIT License

---

## 👨‍💻 Author

**Shubham Salunke**
Full-Stack AI Developer | Medical AI Enthusiast

---




