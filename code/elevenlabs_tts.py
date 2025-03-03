import re
import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play, VoiceSettings
from pydub import AudioSegment
import io
from deep_translator import GoogleTranslator
import sys
from contextlib import redirect_stdout
from file_parser import file_parser
import json

def parse_screenplay(text):
    # Split text into lines and initialize variables
    lines = text.strip().split('\n')
    parsed_parts = []
    current_tag = None
    current_speaker = None
    current_emotion = None
    current_content = ""
    
    for line in lines:
        line = line.strip()
        if not line:  # Skip empty lines
            continue
            
        # Check for tag markers [Tag Name]:
        tag_match = re.match(r'\[(.*?)\]:$', line)
        
        # Don't process as tag if it's a character tag
        if tag_match and not re.match(r'\[((?:Leo|Emma)(?:\s*\((.*?)\))?)\]:$', line):
            # Save previous content if exists
            if current_tag or current_speaker:
                if current_speaker:
                    parsed_parts.append({
                        'type': 'dialogue',
                        'speaker': current_speaker,
                        'emotion': current_emotion,
                        'content': current_content.strip()
                    })
                else:
                    parsed_parts.append({
                        'type': 'description',
                        'tag': current_tag,
                        'content': current_content.strip()
                    })
            
            # Start new tag
            current_tag = tag_match.group(1)
            current_speaker = None
            current_emotion = None
            current_content = ""
            continue
            
        # Check for character dialogue: [Name] or [Name (emotion)]
        speaker_match = re.match(r'\[((?:Leo|Emma)(?:\s*\((.*?)\))?)\]:$', line)
        if speaker_match:
            # Save previous content if exists
            if current_tag or current_speaker:
                if current_speaker:
                    parsed_parts.append({
                        'type': 'dialogue',
                        'speaker': current_speaker,
                        'emotion': current_emotion,
                        'content': current_content.strip()
                    })
                else:
                    parsed_parts.append({
                        'type': 'description',
                        'tag': current_tag,
                        'content': current_content.strip()
                    })
            
            # Start new speaker
            current_tag = None
            speaker_full = speaker_match.group(1)
            if '(' in speaker_full:
                current_speaker = speaker_full.split('(')[0].strip()
                current_emotion = speaker_full.split('(')[1].rstrip(')')
            else:
                current_speaker = speaker_full
                current_emotion = None
            current_content = ""
            continue
        
        # If we reach here, this is content text
        if current_tag or current_speaker:
            current_content += " " + line
    
    # Add the final part if exists
    if current_tag or current_speaker:
        if current_speaker:
            parsed_parts.append({
                'type': 'dialogue',
                'speaker': current_speaker,
                'emotion': current_emotion,
                'content': current_content.strip()
            })
        else:
            parsed_parts.append({
                'type': 'description',
                'tag': current_tag,
                'content': current_content.strip()
            })
    
    return parsed_parts

def get_voice_id(speaker, voice_ids):
    """Get the voice ID for a given speaker."""
    return voice_ids.get(speaker.lower(), None)

def get_voice_settings(emotion):
    """
    Get VoiceSettings object based on emotion.
    Returns VoiceSettings object with appropriate parameters.
    
    Parameters tuned for German emotions:
    - stability: Controls voice consistency (0.0-1.0)
        Lower values = more variation/expressiveness
        Higher values = more stable/consistent
    - similarity_boost: Controls voice authenticity (0.0-1.0)
        Lower values = more room for expression
        Higher values = closer to original voice
    """
    emotion_params = {
        # Besorgt (worried) - moderate variation with high authenticity
        'besorgt': VoiceSettings(
            stability=0.35,           # Some variation to express concern
            similarity_boost=0.75,    # High authenticity for believable worry
            style=0.0, 
            use_speaker_boost=True
        ),
        
        # Flüsternd (whispering) - high variation with moderate authenticity
        'flüsternd': VoiceSettings(
            stability=0.15,           # High variation for whisper effect
            similarity_boost=0.55,    # Lower authenticity to allow for whisper
            style=0.0, 
            use_speaker_boost=True
        ),
        
        # Aufgeregt (excited) - very high variation with moderate authenticity
        'aufgeregt': VoiceSettings(
            stability=0.10,           # Very high variation for excitement
            similarity_boost=0.60,    # Moderate authenticity for natural excitement
            style=0.0, 
            use_speaker_boost=True
        ),
        
        # Ängstlich (anxious) - moderate-high variation with high authenticity
        'ängstlich': VoiceSettings(
            stability=0.25,           # Significant variation for anxiety
            similarity_boost=0.80,    # High authenticity for believable anxiety
            style=0.0, 
            use_speaker_boost=True
        ),
        
        # Default values when no emotion is specified
        None: VoiceSettings(
            stability=0.50,
            similarity_boost=0.50,
            style=0.0,
            use_speaker_boost=True
        )
    }
    
    return emotion_params.get(emotion, emotion_params[None])

def process_dialogue(client, voice_id, speaker, emotion, text):
    # Process each line and collect audio segments
    print(f"Converting ({speaker}{' - ' + emotion if emotion else ''}): {text}")    
    if voice_id:
        try:
            # Get emotion-specific voice settings
            voice_settings = get_voice_settings(emotion)
            
            audio = b''.join(list(client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128",
                voice_settings=voice_settings
            )))
            
            # Convert audio bytes to AudioSegment
            audio_segment = AudioSegment.from_mp3(io.BytesIO(audio))
            
            return audio_segment
            
        except Exception as e:
            print(f"Error converting text to speech for {speaker}: {e}")
    else:
        print(f"No voice ID found for speaker: {speaker}")
    
def translate_to_english(text):
    translator = GoogleTranslator(source='de', target='en')
    return translator.translate(text)

def generate_sound_effect(client, text):
    print("Translating German description...")
    english_text = translate_to_english(text)
    
    print("Generating sound effects...")
    result = client.text_to_sound_effects.convert(
        text=english_text,
        duration_seconds=10,
        prompt_influence=0.3,
    )

    # Combine all chunks into a single bytes object
    audio_data = b''.join(result)

    # convert bytes object into AudioSegment
    audio_segment = AudioSegment.from_mp3(io.BytesIO(audio_data))

    return audio_segment

def run_parser():
    # Create a string buffer to capture the output
    output_buffer = io.StringIO()
    
    # Redirect stdout to our buffer
    with redirect_stdout(output_buffer):
        file_parser()
    
    # Get the captured output as a string
    captured_output = output_buffer.getvalue()
    
    # Close the buffer
    output_buffer.close()
    
    return captured_output

def main():
    # Initialize the client
    load_dotenv()
    api_key = os.getenv("ELEVENLABS_API_KEY")

    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY not found in environment variables")
    
    client = ElevenLabs(api_key=api_key)

    # Map character names to their voice IDs using default voices
    voice_ids = {
        'emma': "21m00Tcm4TlvDq8ikWAM",  # Rachel voice ID
        'leo': "TxGEqnHWrfWFTfGW9XjX",    # Josh voice ID
        'otto': "FTNCalFNG5bRnkkaP5Ug"
    }
    
    parser_output = run_parser()

    parsed_screenplay = parse_screenplay(parser_output)

    pretty_json = json.dumps(parsed_screenplay, indent=4, ensure_ascii=False)
    print(pretty_json)

    # In the highest level, script is divided into two categories: description, dialogue
    # Description has 3 tags: Environment, Background and Additional Description.
    # Dialogue has 2 characters: Emma and Leo.
    combined_audio = AudioSegment.empty()
    silence_duration = AudioSegment.silent(duration=1000)  # ms

    for item in parsed_screenplay:
        # Add silence between lines
        if len(combined_audio) > 0:
            combined_audio += silence_duration
            
        if item['type'] == 'description':
            # Narrator
            if item['tag'] in {"Environment Description", "Additional Description"}:
                voice_id = voice_ids['leo']
                speaker = 'leo'
                emotion = None
                text = item["content"]
                
                combined_audio += process_dialogue(client, voice_id, speaker, emotion, text)
            elif item['tag'] == "Background Description":
                description = item['content']
                combined_audio += generate_sound_effect(client, description)
            else:
                raise ValueError("There is something wrong with the description item!")
        elif item['type'] == 'dialogue':
            _, speaker, emotion, text = item.values()
            voice_id = get_voice_id(speaker, voice_ids)
            combined_audio += process_dialogue(client, voice_id, speaker, emotion, text)
        else:
            raise ValueError("There is something wrong with the dialogue item!")

    # Save the combined audio
    output_filename = "combined_dialogue.mp3"
    combined_audio.export(output_filename, format="mp3")
    print(f"\nSaved combined dialogue to: {output_filename}")

if __name__ == "__main__":
    main()