import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

# 1. Fetch real-time data from a live API (Current weather in London)
print("Fetching real-time data...")
url = "https://api.open-meteo.com/v1/forecast?latitude=51.5074&longitude=-0.1278&current_weather=true"
response = requests.get(url)
realtime_data = response.json()

print(f"Raw Real-Time Data Retrieved: {realtime_data['current_weather']}\n")

# 2. Pass the real-time data directly to OpenAI
prompt = f"""
Here is the current live weather data for London from an API:
{realtime_data['current_weather']}

Please write a friendly 2-sentence weather advisory report based on this live data.
"""

ai_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

# 3. Output the result
print("--- AI Result on Live Data ---")
print(ai_response.choices[0].message.content)