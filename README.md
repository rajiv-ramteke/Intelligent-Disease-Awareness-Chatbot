---
title: HealthBot Pro
emoji: 🏥
colorFrom: indigo
colorTo: blue
sdk: docker
pinned: false
app_port: 7860
---

# HealthBot Pro – Intelligent Disease Awareness Chatbot

HealthBot Pro is a production-ready, deployment-friendly AI healthcare awareness chatbot web application. It is designed to be easily deployable, scalable, and serves as an excellent final-year engineering project.

## Features
- **AI Health Assistant**: Context-aware chatbot using NVIDIA's Llama models to provide health awareness without diagnosing.
- **Multilingual Support**: Supports English, Hindi, and Marathi natively.
- **Voice Assistant**: Integrated Browser Web Speech API for TTS and STT.
- **Disease Awareness Module**: Knowledge base integration for major diseases.
- **Emergency Detection**: Identifies critical symptoms (e.g., chest pain, bleeding) and triggers alerts.
- **Location Services**: Integrates with Google Maps API to find nearby healthcare facilities.
- **Admin Dashboard**: Monitors traffic, alerts, and system health.

## Setup & Local Execution
1. Clone the repository.
2. Create a `.env` file based on `.env.example` and add your NVIDIA and Google Maps API keys.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   flask run --port=8000
   ```

## Docker Deployment
```bash
docker-compose up --build
```

## Render Deployment
Simply connect this repository to Render and use the provided `render.yaml` Blueprint to automatically provision and deploy the application.
