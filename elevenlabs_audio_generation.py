from dotenv import load_dotenv
import os
from elevenlabs.client import ElevenLabs
from elevenlabs import play
from pydub import AudioSegment
import io
from deep_translator import GoogleTranslator

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

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("ELEVENLABS_API_KEY")
    client = ElevenLabs(api_key=api_key)
    
    description = "Ein hochfrequenter Ton vermischt sich mit dem Brüllen, wird langsam lauter und klingt fast wie das Dröhnen eines Motors."
    
    audio_data = generate_sound_effect(client, description)

    play(audio_data.export(format="mp3").read())

    audio_data.export("output.mp3", format="mp3")