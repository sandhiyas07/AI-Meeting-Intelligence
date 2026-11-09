
"""
AI Meeting Intelligence
Gemini Audio Analysis Service
"""

import os
import json
import re

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# API Key
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing in .env file")

# Gemini client
client = genai.Client(api_key=API_KEY)


# -----------------------------------
# FIND AVAILABLE GEMINI MODEL
# -----------------------------------

def get_available_model():

    try:
        print("Checking available Gemini models...")

        available_models = client.models.list()

        supported_models = {}

        for model in available_models:

            name = getattr(model, "name", "") or ""

            actions = getattr(model, "supported_actions", []) or []

            if "generateContent" in actions:

                clean_name = name.replace("models/", "")

                supported_models[clean_name] = clean_name

        print("Available models:", list(supported_models.keys()))

        # First try model configured in .env
        preferred = os.getenv("GEMINI_MODEL", "").strip()

        if preferred:
            preferred = preferred.replace("models/", "")

            if preferred in supported_models:
                print("Using configured model:", preferred)
                return preferred

            print("Configured model unavailable:", preferred)

        # Automatically select an available model
        candidates = [
            "gemini-3.8-flash",
            "gemini-3.5-flash-lite"
        ]

        for candidate in candidates:

            if candidate in supported_models:
                print("Selected model:", candidate)
                return candidate

        # Use another available Gemini model
        for name in supported_models:

            if "gemini" in name.lower():
                print("Using available fallback:", name)
                return name

        raise RuntimeError(
            "No Gemini model supporting generateContent was found."
        )

    except Exception as error:

        raise RuntimeError(
            f"Could not retrieve available Gemini models: {error}"
        ) from error


# -----------------------------------
# MEETING AUDIO ANALYSIS
# -----------------------------------

def analyze_meeting_audio(
    audio_bytes,
    filename,
    language="English",
    detail="Medium"
):

    try:

        if not audio_bytes:
            raise ValueError("Please upload an audio recording.")

        if len(audio_bytes) > 20 * 1024 * 1024:
            raise ValueError("Audio file must be smaller than 20 MB.")

        extension = os.path.splitext(filename)[1].lower()

        audio_formats = {
            ".wav": "audio/wav",
            ".mp3": "audio/mpeg",
            ".m4a": "audio/mp4"
        }

        if extension not in audio_formats:
            raise ValueError("Unsupported audio format.")

        mime_type = audio_formats[extension]

        # Get a model supported by this API key
        model_name = get_available_model()

        # Summary detail
        detail_options = {
            "Short": "Write a short summary.",
            "Medium": "Write a clear summary with important details.",
            "Detailed": "Write a comprehensive meeting summary."
        }

        summary_style = detail_options.get(
            detail,
            detail_options["Medium"]
        )

        # AI prompt
        prompt = f"""
You are an expert AI Meeting Intelligence Assistant.

Analyze the attached meeting audio.

Language: {language}

Tasks:

1. TRANSCRIPT:
Convert the spoken conversation into text.
Preserve the actual meaning.
Do not invent conversations.

2. SUMMARY:
{summary_style}
Explain the purpose and outcome of the meeting.

3. KEY POINTS:
Extract all important discussion points and decisions.

4. ACTION ITEMS:
Identify tasks, responsible persons and deadlines.
Do not invent names or deadlines.

Return ONLY valid JSON.

Use this exact format:

{{
    "transcript": "Full meeting transcript",
    "summary": "Meeting summary",
    "key_points": [
        "Important point 1",
        "Important point 2"
    ],
    "action_items": [
        {{
            "task": "Task description",
            "assigned_to": "Person name or Not specified",
            "deadline": "Deadline or Not specified"
        }}
    ]
}}
"""

        # Audio input
        audio_part = types.Part.from_bytes(
            data=audio_bytes,
            mime_type=mime_type
        )

        # Generate response
        print("Sending audio to Gemini:", model_name)

        response = client.models.generate_content(
            model=model_name,
            contents=[
                prompt,
                audio_part
            ],
            config=types.GenerateContentConfig(
                temperature=0.2,
                response_mime_type="application/json"
            )
        )

        response_text = response.text

        if not response_text:
            raise ValueError("Gemini returned an empty response.")

        # Clean JSON
        response_text = response_text.strip()

        response_text = re.sub(
            r"^```(?:json)?\s*",
            "",
            response_text
        )

        response_text = re.sub(
            r"\s*```$",
            "",
            response_text
        )

        # Parse response
        result = json.loads(response_text)

        if not isinstance(result, dict):
            raise ValueError("Invalid Gemini response.")

        # Validate response
        transcript = result.get("transcript", "")
        summary = result.get("summary", "")
        key_points = result.get("key_points", [])
        action_items = result.get("action_items", [])

        if not isinstance(transcript, str):
            raise ValueError("Invalid transcript.")

        if not isinstance(summary, str):
            raise ValueError("Invalid summary.")

        if not isinstance(key_points, list):
            raise ValueError("Invalid key points.")

        if not isinstance(action_items, list):
            raise ValueError("Invalid action items.")

        print("Meeting analysis completed successfully.")

        return {
            "transcript": transcript,
            "summary": summary,
            "key_points": key_points,
            "action_items": action_items
        }

    except Exception as error:

        print("Gemini analysis error:", str(error))

        raise RuntimeError(
            f"Meeting analysis error: {error}"
        ) from error
