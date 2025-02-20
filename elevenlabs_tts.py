import re
import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play, VoiceSettings
from pydub import AudioSegment
import io

def parse_dialogue(text):
    lines = text.strip().split('\n')
    dialogue_parts = []
    current_speaker = None
    current_emotion = None
    current_line = ""
    
    for line in lines:
        line = line.strip()
        if not line:  # Skip empty lines
            continue
            
        # Pattern to match: Character name followed by optional emotion in parentheses
        speaker_match = re.match(r'(\w+)(?:\s*\((.*?)\))?$', line)
        
        if speaker_match:
            # If we have a previous speaker and line, save it before starting new one
            if current_speaker and current_line:
                dialogue_parts.append((current_speaker, current_emotion, current_line.strip()))
            
            # Start new speaker, emotion, and line
            current_speaker = speaker_match.group(1)
            current_emotion = speaker_match.group(2) if speaker_match.group(2) else None
            current_line = ""
        else:
            # If no speaker match, this is dialogue text
            if current_speaker:
                current_line += " " + line
    
    # Add the last dialogue part if exists
    if current_speaker and current_line:
        dialogue_parts.append((current_speaker, current_emotion, current_line.strip()))
    
    return dialogue_parts

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
        'leo': "TxGEqnHWrfWFTfGW9XjX"    # Josh voice ID
    }

    dialogue = """
    Emma (besorgt)
    Leo, ich hab ein really bad feeling about this!
    Leo
    Bleib ruhig. Ich glaube… es aktiviert sich… oder so was.
    Emma
    Oder so was? Das ist nicht beruhigend!
    """

    dialogue_parts = parse_dialogue(dialogue)

    # Process each line and collect audio segments
    combined_audio = AudioSegment.empty()
    silence = AudioSegment.silent(duration=1000)  # 1 second silence between lines

    for speaker, emotion, text in dialogue_parts:
        print(f"Converting ({speaker}{' - ' + emotion if emotion else ''}): {text}")
        
        voice_id = get_voice_id(speaker, voice_ids)
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
                
                # Add silence between lines
                if len(combined_audio) > 0:
                    combined_audio += silence
                
                # Add the new audio segment
                combined_audio += audio_segment
                
            except Exception as e:
                print(f"Error converting text to speech for {speaker}: {e}")
        else:
            print(f"No voice ID found for speaker: {speaker}")

    # Save the combined audio
    output_filename = "combined_dialogue.mp3"
    combined_audio.export(output_filename, format="mp3")
    print(f"\nSaved combined dialogue to: {output_filename}")
    
    play(combined_audio.export(format="mp3").read())

if __name__ == "__main__":
    main()