import re
import os
import boto3
from dotenv import load_dotenv
from pydub import AudioSegment
import io

def parse_dialogue(text):
    """Parse dialogue with emotion tags"""
    lines = text.strip().split('\n')
    dialogue_parts = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:  # Skip empty lines
            i += 1
            continue
            
        # Check for speaker line with potential emotion
        speaker_match = re.match(r'(\w+)(?:\s*\((.*?)\))?$', line)
        if speaker_match:
            speaker = speaker_match.group(1)
            emotion = speaker_match.group(2) if speaker_match.group(2) else None
            
            # Look for the next non-empty line as the dialogue
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
                
            if i < len(lines):
                dialogue_line = lines[i].strip()
                dialogue_parts.append((speaker, dialogue_line, emotion))
        i += 1
    
    return dialogue_parts

def get_ssml_with_emotion(text, emotion=None):
    """Generate SSML text with supported tags based on emotion"""
    # Escape special characters for SSML
    text = text.replace('&', '&amp;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&apos;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    
    if emotion and emotion.lower() == 'besorgt':  # worried
        # Add breaks and sentence structure for worried tone
        ssml = (
            '<speak><p><s>'
            f'{text}<break time="300ms"/>'
            '</s></p></speak>'
        )
    else:
        ssml = f'<speak><p><s>{text}</s></p></speak>'
    
    return ssml

def synthesize_speech(polly_client, text, voice_id, emotion=None):
    """Synthesize speech using Amazon Polly and return AudioSegment"""
    try:
        ssml = get_ssml_with_emotion(text, emotion)
        print(f"Using SSML: {ssml}")
        
        response = polly_client.synthesize_speech(
            VoiceId=voice_id,
            OutputFormat='mp3',
            Text=ssml,
            TextType='ssml',
            Engine='neural',
            LanguageCode='de-DE'
        )
        
        # Convert the audio stream to AudioSegment
        audio_stream = io.BytesIO(response['AudioStream'].read())
        return AudioSegment.from_mp3(audio_stream)
        
    except Exception as e:
        print(f"Error synthesizing speech: {str(e)}")
        print("Retrying without SSML...")
        try:
            response = polly_client.synthesize_speech(
                VoiceId=voice_id,
                OutputFormat='mp3',
                Text=text,
                TextType='text',
                Engine='neural',
                LanguageCode='de-DE'
            )
            audio_stream = io.BytesIO(response['AudioStream'].read())
            return AudioSegment.from_mp3(audio_stream)
        except Exception as e:
            print(f"Error with plain text synthesis: {str(e)}")
            return AudioSegment.silent(duration=500)

def main():
    load_dotenv()

    dialogue = """
    Emma (besorgt)
    Leo, ich hab ein really bad feeling about this!
    Leo
    Bleib ruhig. Ich glaube… es aktiviert sich… oder so was.
    Emma
    Oder so was? Das ist nicht beruhigend!
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
    pause = AudioSegment.silent(duration=500)  # 500ms pause

    # Process each line of dialogue
    for speaker, text, emotion in dialogue_parts:
        print(f"Processing: {speaker}{' (' + emotion + ')' if emotion else ''}: {text}")
        
        # Get the appropriate voice for the speaker
        voice_id = voice_mapping.get(speaker)
        if not voice_id:
            print(f"Warning: No voice mapping for {speaker}, skipping...")
            continue
            
        # Synthesize the line with emotion if specified
        audio_segment = synthesize_speech(polly_client, text, voice_id, emotion)
        
        # Add to combined audio with pause
        combined_audio += audio_segment + pause

    # Export the final audio file
    output_file = "aws_output.mp3"
    combined_audio.export(output_file, format="mp3")
    print(f"Audio saved to {output_file}")

if __name__ == "__main__":
    main()