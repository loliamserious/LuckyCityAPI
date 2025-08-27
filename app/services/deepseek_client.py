import os
import json
from typing import Dict
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

# Initialize OpenAI client with Deepseek's base URL
client = AsyncOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

async def get_predictions(birthday: str, country: str) -> Dict:
    prompt = f"""
    Based on the birthday {birthday}, perform the following tasks:

    1. Calculate the Four Pillars of Destiny (八字) - Year Pillar, Month Pillar, Day Pillar, and Hour Pillar in Chinese characters.
    2. Calculate the percentage distribution of the Five Elements (五行) in the Four Pillars.
    3. Using these Four Pillars, recommend the top 5 most suitable cities in {country} for this person to live.

    Consider the following factors in your city analysis:
    1. The energy and elements represented in the Four Pillars
    2. The dominant elements of each recommended city
    3. The compatibility between the person's Five Elements distribution and each city's elements
    4. The potential for personal growth and success in each location based on elemental harmony

    Format your response as a JSON object with exactly this structure:
    {{
        "four_pillars": "The Four Pillars in Chinese characters",
        "elements_analysis": {
            "wood": 25,
            "fire": 20,
            "earth": 15,
            "metal": 25,
            "water": 15
        },
        "predictions": [
            {{
                "city": "City Name",
                "rate": 95,
                "reason": "First reason sentence. Second reason sentence.",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "dominant_elements": ["wood", "water"]
            }},
            ... (4 more cities)
        ]
    }}

    Requirements:
    - The "predictions" array must contain exactly 5 cities
    - Each "rate" must be between 1 and 100 percentage
    - Each "reason" must be exactly two sentences
    - Each city must include accurate latitude and longitude coordinates
    - The elements_analysis percentages must sum to 100
    - Each city must have 1-3 dominant elements listed
    - Return only the JSON object, no additional text or explanation
    """
    
    response = await client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are an expert in Chinese astrology and geography, with precise knowledge of city locations and coordinates."},
            {"role": "user", "content": prompt}
        ],
        stream=False
    )
    
    result = json.loads(response.choices[0].message.content)
    return result 