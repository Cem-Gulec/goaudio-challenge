import re
import os
import boto3
from dotenv import load_dotenv

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

    dialogue_parts = parse_dialogue(dialogue)

    for line in dialogue_parts:
        print(f"{line}\n")

    polly_client = boto3.Session(
        aws_access_key_id=os.getenv("aws_access_key_id"),                     
        aws_secret_access_key=os.getenv("aws_secret_access_key"),
        region_name='us-west-2').client('polly')

    response = polly_client.synthesize_speech(VoiceId='Joanna',
                    OutputFormat='mp3', 
                    Text = 'This is a sample text to be synthesized.',
                    Engine = 'neural')

    file = open('speech.mp3', 'wb')
    file.write(response['AudioStream'].read())
    file.close()

if __name__ == "__main__":
    main()