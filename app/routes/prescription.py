import base64
import json
import re
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import requests
import os

router = APIRouter(prefix="/prescription", tags=["Prescription"])

OPENAI_API_KEY = "provide key here"
#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


@router.post("/analyze")
async def analyze_prescription_file(file: UploadFile = File(...)):
    try:
        # 1️⃣ Read file and convert to base64
        file_bytes = await file.read()
        base64_image = base64.b64encode(file_bytes).decode("utf-8")
        data_url = f"data:{file.content_type};base64,{base64_image}"

        # 2️⃣ Prompt for OpenAI
        prompt_text = """
You are a medical assistant. Extract all medicines from this prescription image.
For each medicine, provide:
- name
- dosage
- usage (purpose)
- common side effects
Return strictly as JSON only, without any markdown code block.
"""

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "user", "content": [{"type": "text", "text": prompt_text},
                                              {"type": "image_url", "image_url": {"url": data_url}}]}
            ],
        }

        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }

        # 3️⃣ Call OpenAI
        response = requests.post(OPENAI_API_URL, headers=headers, json=payload)
        response_json = response.json()

        # 4️⃣ Extract message content
        summary_text = response_json["choices"][0]["message"]["content"]

        # 5️⃣ Optional: remove ```json wrapper if any
        clean_text = re.sub(r"```json|```", "", summary_text).strip()

        # 6️⃣ Convert to dict
        summary_json = json.loads(clean_text)

        return JSONResponse(content=summary_json)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)