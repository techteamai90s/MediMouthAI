from openai import OpenAI
from app.config import settings


def get_client():
    if not settings.OPENAI_API_KEY:
        raise ValueError("❌ OPENAI_API_KEY not found. Please check your .env or environment variables.")
    return OpenAI(api_key=settings.OPENAI_API_KEY)


async def analyze_prescription(file_path: str):
    client = get_client()  # create client only when needed

    with open(file_path, "rb") as f:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a medical assistant. Extract medicines, their usage and side effects from doctor prescriptions."
                },
                {
                    "role": "user",
                    "content": "Analyze this prescription and extract medicine details."
                }
            ],
            max_tokens=500,
        )

    return response.choices[0].message["content"]