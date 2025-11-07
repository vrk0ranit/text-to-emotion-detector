import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Allow frontend requests (keep open for now)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hugging Face API endpoint and token
HF_API_URL = "https://api-inference.huggingface.co/models/bhadresh-savani/distilbert-base-uncased-emotion"
HF_TOKEN = os.environ.get("HF_TOKEN")  # we’ll add this in Render dashboard

# Input model
class TextInput(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "Emotion Detector API (via Hugging Face) is running 🚀"}

@app.post("/predict")
def predict_emotion(input: TextInput):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": input.text}

    response = requests.post(HF_API_URL, headers=headers, json=payload)
    result = response.json()

    # Handle API errors gracefully
    if isinstance(result, dict) and "error" in result:
        return {"error": result["error"]}

    # Pick top emotion
    emotion = max(result[0], key=lambda x: x["score"])
    return {"label": emotion["label"], "score": round(emotion["score"], 3)}

# ✅ Proper Render port binding
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
