import openai
import argparse
import os
import json

def generate_hooks(transcription, api_key, model="gpt-4o"):
    """
    Analyzes transcription and generates 5 high-converting hooks for Reels.
    Uses AI to identify key selling points and emotional triggers.
    """
    print(f"[*] Analyzing transcription (length: {len(transcription)})...")
    
    client = openai.OpenAI(api_key=api_key)
    
    prompt = f"""
    You are a professional social media marketing expert. 
    Analyze the following video transcription and generate 5 different 'Hooks' (first 3-5 seconds of a video).
    
    The goal is to maximize audience retention and curiosity.
    Each hook should have:
    1. A 'Headline' (text overlay)
    2. A 'Visual description' of what should happen on screen.
    
    Transcription:
    \"\"\"{transcription}\"\"\"
    
    Return the result as a JSON array of objects with keys: headline, visual_description.
    """

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    result = json.loads(response.choices[0].message.content)
    print(f"[+] Generated {len(result['hooks'])} hooks.")
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Hook Generator for Content Creators")
    parser.add_argument("--transcription", required=True, help="Transcription text from video")
    parser.add_argument("--key", required=True, help="OpenAI API Key")
    parser.add_argument("--output", default="hooks.json", help="Path to save generated hooks")
    
    args = parser.parse_args()
    
    hooks = generate_hooks(args.transcription, args.key)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(hooks, f, indent=2, ensure_ascii=False)
    print(f"[+] Hooks saved to: {args.output}")
