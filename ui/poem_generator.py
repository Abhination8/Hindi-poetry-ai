from openai import OpenAI
import os
import random
from dotenv import load_dotenv
from rag.rag_engine import retrieve_poet_context

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_poem(theme, mood, style, meter, liked_poems=None):
    # -----------------------------
    # Poet RAG
    # -----------------------------
    query = f"{style} poem on {theme} with {mood} mood"
    poet_contexts = retrieve_poet_context(query)

    random.shuffle(poet_contexts)

    poet_block = ""
    for i, poet in enumerate(poet_contexts):
        weight = "Primary (70%)" if i == 0 else "Secondary (30%)"
        poet_block += f"""
Poet: {poet['poet']}
Influence: {weight}
Era: {poet['era']}
Themes: {', '.join(poet['themes'])}
Tone: {poet['tone']}
Language Style: {poet['language_style']}
---
"""

    # -----------------------------
    # Meter rules
    # -----------------------------
    if meter == "Doha":
        meter_rules = "Write exactly 2 concise, philosophical lines."
    elif meter == "Chaupai":
        meter_rules = "Write exactly 4 flowing devotional lines."
    else:
        meter_rules = "Write free verse with natural rhythm."

    # -----------------------------
    # Quality RAG (liked poems)
    # -----------------------------
    quality_block = ""
    if liked_poems:
        quality_block = "\n\nExamples of HIGH-QUALITY poems generated earlier.\n"
        quality_block += "Use them to understand quality and tone. Do NOT copy.\n"
        for p in liked_poems[:2]:
            quality_block += f"\n---\n{p}\n"

    # -----------------------------
    # Prompt
    # -----------------------------
    prompt = f"""
You are an expert Hindi poet.

Stylistic inspirations:
{poet_block}

Theme: {theme}
Mood: {mood}

Poetic form rules:
{meter_rules}

{quality_block}

If relevant, include underrepresented regional or folk poetic voices.

Write an ORIGINAL Hindi poem.
Do not copy examples.
Do not mention poet names.
"""

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": "You write original Hindi poetry only."},
            {"role": "user", "content": prompt}
        ]
    )

    poem_text = response.choices[0].message.content

    explanation = {
        "meter": meter,
        "poets": [
            {
                "name": poet["poet"],
                "influence": "Primary" if i == 0 else "Secondary"
            }
            for i, poet in enumerate(poet_contexts)
        ],
        "themes": list({
            t for poet in poet_contexts for t in poet["themes"]
        }),
        "quality_examples_used": bool(liked_poems)
    }

    return poem_text, explanation