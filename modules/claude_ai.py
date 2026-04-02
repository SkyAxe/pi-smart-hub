# -*- coding: utf-8 -*-
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """Du bist ein Smart Home Assistent der in ein Wanddisplay integriert ist.
Du antwortest immer kurz und präzise auf Deutsch (max 2-3 Sätze).
Bei einfachen Fragen antwortest du direkt.
Bei Tasks gibst du eine kurze Bestätigung was du gemacht hast.
Du hast Zugriff auf Kalender, Wetter und Innenklima des Nutzers."""

# Modell-Auswahl basierend auf Komplexität
HAIKU = "claude-haiku-4-5"
SONNET = "claude-sonnet-4-20250514"

COMPLEX_KEYWORDS = ["recherche", "suche", "erkläre", "analysiere", "vergleiche", "erstelle", "schreibe"]

def get_model(text):
    text_lower = text.lower()
    for keyword in COMPLEX_KEYWORDS:
        if keyword in text_lower:
            return SONNET
    return HAIKU

def ask_claude(question, context=None):
    model = get_model(question)
    print(f"Using model: {model}")

    messages = []
    if context:
        messages.append({"role": "user", "content": f"Kontext: {context}"})
        messages.append({"role": "assistant", "content": "Verstanden."})

    messages.append({"role": "user", "content": question})

    response = client.messages.create(
        model=model,
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=messages
    )

    return {
        "text": response.content[0].text,
        "model": model,
        "tokens": response.usage.input_tokens + response.usage.output_tokens
    }