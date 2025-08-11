import os
import json
from typing import Dict
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Initialize OpenAI client with Deepseek's base URL
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

async def get_predictions(birthday: str, country: str) -> Dict:
    prompt = f"""
    Based on the birthday {birthday}, perform the following tasks:

    1. Calculate the Four Pillars of Destiny (八字) - Year Pillar, Month Pillar, Day Pillar, and Hour Pillar in Chinese characters.
    2. Using these Four Pillars, recommend the top 5 most suitable cities in {country} for this person to live.

    Consider the following factors in your city analysis:
    1. The energy and elements represented in the Four Pillars
    2. The potential for personal growth and success in each location based on the Four Pillars

    Format your response as a JSON object with exactly this structure:
    {{
        "four_pillars": "The Four Pillars in Chinese characters",
        "predictions": [
            {{
                "city": "City Name",
                "rate": 95,
                "reason": "First reason sentence. Second reason sentence."
            }},
            ... (4 more cities)
        ]
    }}

    Requirements:
    - The "predictions" array must contain exactly 5 cities
    - Each "rate" must be between 1 and 100 precentage
    - Each "reason" must be exactly two sentences
    - Return only the JSON object, no additional text or explanation
    """
    
    response = await client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are an expert in Chinese astrology."},
            {"role": "user", "content": prompt}
        ],
        stream=False
    )
    
    result = json.loads(response.choices[0].message.content)
    return result 