import json
import os

DATA_PATH = os.path.join("ui", "rag", "hindi_poets.json")


def retrieve_poet_context(query, meter=None, top_k=3):
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        poets = json.load(f)

    # Simple semantic-like filtering (MVP-safe)
    scored = []
    query_lower = query.lower()

    for poet in poets:
        score = 0
        for theme in poet.get("themes", []):
            if theme.lower() in query_lower:
                score += 2
        if poet.get("era", "").lower() in query_lower:
            score += 1
        scored.append((score, poet))

    scored.sort(key=lambda x: x[0], reverse=True)
    results = [p for _, p in scored[:top_k]]

    # Meter-aware boost
    if meter:
        preferred = [
            p for p in results
            if meter in p.get("meter_preference", [])
        ]
        if preferred:
            results = preferred + results

    return results[:top_k]