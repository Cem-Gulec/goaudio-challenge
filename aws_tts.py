import re
import os
import boto3
from dotenv import load_dotenv
from pydub import AudioSegment
import io

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

def synthesize_speech(polly_client, text, voice_id):
    """Synthesize speech using Amazon Polly and return AudioSegment"""
    response = polly_client.synthesize_speech(
        VoiceId=voice_id,
        OutputFormat='mp3',
        Text=text,
        Engine='neural',
        LanguageCode='de-DE'
    )
    
    # Convert the audio stream to AudioSegment
    audio_stream = io.BytesIO(response['AudioStream'].read())
    return AudioSegment.from_mp3(audio_stream)

def main():
    load_dotenv()

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

    # Define voice mapping
    voice_mapping = {
        'Emma': 'Vicki',  # German female voice
        'Leo': 'Daniel'   # German male voice
    }

    dialogue_parts = parse_dialogue(dialogue)

    # Initialize Polly client
    polly_client = boto3.Session(
        aws_access_key_id=os.getenv("aws_access_key_id"),
        aws_secret_access_key=os.getenv("aws_secret_access_key"),
        region_name='us-west-2'
    ).client('polly')

    # Initialize combined audio
    combined_audio = AudioSegment.empty()
    
    # Add small pause between lines
    pause = AudioSegment.silent(duration=50) 

    # Process each line of dialogue
    for speaker, text in dialogue_parts:
        print(f"Processing: {speaker}: {text}")
        
        # Get the appropriate voice for the speaker
        voice_id = voice_mapping.get(speaker)
        if not voice_id:
            print(f"Warning: No voice mapping for {speaker}, skipping...")
            continue
            
        # Synthesize the line
        audio_segment = synthesize_speech(polly_client, text, voice_id)
        
        # Add to combined audio with pause
        combined_audio += audio_segment + pause

    # Export the final audio file
    output_file = "dialogue.mp3"
    combined_audio.export(output_file, format="mp3")
    print(f"Audio saved to {output_file}")

if __name__ == "__main__":
    main()