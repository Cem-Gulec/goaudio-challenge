import re
import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play

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
    # Initialize the client
    load_dotenv()
    api_key = os.getenv("ELEVENLABS_API_KEY")

    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY not found in environment variables")
    
    client = ElevenLabs(api_key=api_key)

    emma_voice_id = "nF7t9cuYo0u3kuVI9q4B"
    leo_voice_id = "LBdEwXpO9YwPdF4PqCd9"
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

    audio = client.text_to_speech.convert(
        text="The first move is what sets everything in motion.",
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    play(audio)


if __name__ == "__main__":
    main()