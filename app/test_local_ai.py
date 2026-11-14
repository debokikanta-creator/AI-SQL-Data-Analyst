
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url=os.getenv("LOCAL_AI_BASE_URL"),
    api_key="lm-studio"
)

model = os.getenv("LOCAL_AI_MODEL")

try:
    print("Connecting to local AI...")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": (
                    "You are a SQL data analyst. "
                    "Write a SQLite query to calculate "
                    "total revenue from the orders table "
                    "using the amount column. "
                    "Return SQL only."
                )
            }
        ],
        temperature=0.1,
        max_tokens=200
    )

    print("\nLOCAL AI CONNECTION SUCCESSFUL!")
    print("\nGenerated SQL:")
    print(response.choices[0].message.content)

except Exception as e:
    print("\nLOCAL AI ERROR:")
    print(type(e).__name__, str(e))
