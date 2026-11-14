
from sql_generator import client, model


def explain_results(question, sql, results):

    # Convert database results into readable text
    if results.empty:
        result_text = "The query returned no records."
    else:
        result_text = results.head(20).to_string(index=False)

    # Prepare prompt for local Qwen3 model
    prompt = f"""
You are an experienced business data analyst.

A user asked this question:
{question}

The SQL query executed was:
{sql}

The actual database results are:
{result_text}

Total rows returned: {len(results)}

Your task:

1. Explain the results in simple English.
2. Directly answer the user's question.
3. Highlight important numbers and patterns.
4. Explain what the results mean for the business.
5. Do not invent facts or statistics.
6. Do not make assumptions unsupported by the results.
7. If the results are empty, explain that clearly.
8. Keep your explanation concise and professional.

IMPORTANT:
Use only the actual database results.
Do not invent additional data.

Write your explanation in natural language.
"""

    # Ask local Qwen3 to explain the results
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=400
    )

    explanation = response.choices[0].message.content

    if not explanation or not explanation.strip():
        raise ValueError("The AI returned an empty explanation.")

    return explanation.strip()

    if not explanation:
        raise ValueError("The AI returned an empty explanation.")

    return explanation.strip()
