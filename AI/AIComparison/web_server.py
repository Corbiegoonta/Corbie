from fastapi import FastAPI, Request
from dotenv import load_dotenv
import requests
import os
import uvicorn

app = FastAPI()

load_dotenv()

# 🔐 Replace this with your actual Hugging Face API token
HF_API_KEY = os.getenv("HUGGINGFACE_KEY") 
HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

@app.post("/compare")
async def compare_models(request: Request):
    data = await request.json()
    prompt = data.get("Hello World")

    # 📨 Construct the payload for Hugging Face Inference API
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 100
        }
    }

    # 📡 Make the POST request to Hugging Face
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    print("Hugging Face Response: ", response)
    # Check for errors
    if response.status_code != 200:
        return {
            "error": f"Hugging Face API returned status code {response.status_code}",
            "details": response.text
        }

    output = response.json()
    print("Hugging Face Output: ", output)

    # res = {
    #     "mistral": output[0]["generated_text"] if isinstance(output, list) else str(output),
    #     "openai": "Stub",
    #     "claude": "Stub"
    # }

    # print(res)

    # return res

if __name__ == "__main__":
    uvicorn.run(app, reload=True)

