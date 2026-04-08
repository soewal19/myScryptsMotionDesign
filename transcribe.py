import os
import sys
import whisper
import argparse

def transcribe(video_path, output_srt, model_size="base"):
    print(f"Loading Whisper model: {model_size}...")
    model = whisper.load_model(model_size)
    
    print(f"Transcribing: {video_path}")
    result = model.transcribe(video_path, verbose=False)
    
    print(f"Saving to: {output_srt}")
    with open(output_srt, "w", encoding="utf-8") as srt:
        for i, segment in enumerate(result['segments']):
            start = format_timestamp(segment['start'])
            end = format_timestamp(segment['end'])
            text = segment['text'].strip()
            
            srt.write(f"{i + 1}\n")
            srt.write(f"{start} --> {end}\n")
            srt.write(f"{text}\n\n")
    
    print("Done!")

def format_timestamp(seconds: float):
    td = float(seconds)
    hours = int(td // 3600)
    minutes = int((td % 3600) // 60)
    secs = int(td % 60)
    msecs = int((td % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{msecs:03}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe video to SRT using Whisper")
    parser.add_argument("input", help="Path to video/audio file")
    parser.add_argument("--output", help="Path to output SRT", default=None)
    parser.add_argument("--model", help="Whisper model (tiny, base, small, medium, large)", default="base")
    
    args = parser.parse_args()
    
    input_path = args.input
    output_path = args.output or os.path.splitext(input_path)[0] + ".srt"
    
    if not os.path.exists(input_path):
        print(f"Error: File not found {input_path}")
        sys.exit(1)
        
    transcribe(input_path, output_path, args.model)
