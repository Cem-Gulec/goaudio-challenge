from dotenv import load_dotenv
import os
from elevenlabs.client import ElevenLabs
from elevenlabs import play
from pydub import AudioSegment
import io

def generate_sound_effect(client, text):
    print("Generating sound effects...")

    result = client.text_to_sound_effects.convert(
        text=text,
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
    
    description = "A high-pitched sound mingles with the roar, slowly increasing and sounding almost like the roar of an engine."
    
    audio_data = generate_sound_effect(client, description)

    play(audio_data.export(format="mp3").read())

    audio_data.export("output.mp3", format="mp3")