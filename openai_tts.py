import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import re
from pydub import AudioSegment
import wave
import io

# Function to split dialogue into character lines
def parse_dialogue(text):
    lines = text.strip().split('\n')
    current_speaker = None
    dialogue_parts = []
    current_line = ""
    
    for line in lines:
        line = line.strip()
        if not line:  # Skip empty lines
            continue
            
        speaker_match = re.match(r'\[(\w+)\]:', line)
        if speaker_match:
            # If we have a previous speaker and line, save it before starting new one
            if current_speaker and current_line:
                dialogue_parts.append((current_speaker, current_line.strip()))
            
            # Start new speaker and line
            current_speaker = speaker_match.group(1)
            # Remove the speaker tag from the line
            current_line = re.sub(r'\[\w+\]:', '', line).strip()
        else:
            # Only append to current line if we have a current speaker
            if current_speaker:
                current_line += " " + line
    
    if current_speaker and current_line:
        dialogue_parts.append((current_speaker, current_line.strip()))
    
    return dialogue_parts

def main():
    # initialize the OpenAI API client
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    dialogue = """
    [Emma]:
    Also, Leo, was hast du mir hier überhaupt zeigen wollen?

    [Leo]:
    Geduld, Emma. Es ist ein bisschen… wie soll ich sagen… next-level cool.

    [Emma]:
    Deine Überraschungen waren nicht immer cool. Erinnere dich an die „Super-Höhle“ voller Spinnen.

    [Leo]:
    Hey, das war ein Abenteuer! Und diesmal gibt’s keine Spinnen. Versprochen.
    """

    dialogue_parts = parse_dialogue(dialogue)

    for line in dialogue_parts:
        print(f"{line}\n")

    # Generate and collect all audio data
    all_audio_data = []
    for speaker, line in dialogue_parts:
        # Choose voice based on speaker
        voice = "nova" if speaker == "Emma" else "onyx"
        
        # Generate speech for the line
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=line,
            speed=1.0,
            response_format="mp3"
        )
        
        # Get the audio data
        audio_data = response.content
        all_audio_data.append(audio_data)

    # Write all audio data to a single file
    with open("openai_output.mp3", "wb") as outfile:
        for audio_data in all_audio_data:
            outfile.write(audio_data)

if __name__ == "__main__":
    main()