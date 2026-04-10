import requests
import json
import argparse
import os

def generate_voiceover(text, voice_id, api_key, output_path):
    """
    Generates high-quality voiceover using ElevenLabs API.
    Supports 29 languages with emotional consistency.
    """
    print(f"[*] Generating voiceover for: {text[:50]}...")
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.5,
            "use_speaker_boost": True
        }
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"[+] Voiceover saved to: {output_path}")
        return True
    else:
        print(f"[!] API Error: {response.text}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ElevenLabs TTS Generator for Localization")
    parser.add_argument("--text", required=True, help="Text to convert to speech")
    parser.add_argument("--voice_id", default="21m00Tcm4TlvDq8ikWAM", help="ElevenLabs Voice ID")
    parser.add_argument("--key", required=True, help="ElevenLabs API Key")
    parser.add_argument("--output", required=True, help="Output MP3 path")
    
    args = parser.parse_args()
    generate_voiceover(args.text, args.voice_id, args.key, args.output)
