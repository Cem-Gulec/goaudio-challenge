from dotenv import load_dotenv
import os
from elevenlabs.client import ElevenLabs

def generate_sound_effect(client, text):
    print("Generating sound effects...")

    result = client.text_to_sound_effects.convert(
        text=text,
        duration_seconds=10,
        prompt_influence=0.3,
    )

    # Combine all chunks into a single bytes object
    audio_data = b''.join(result)
    return audio_data

def save_audio(audio_data: bytes, output_path: str):
    with open(output_path, "wb") as f:
        f.write(audio_data)
    print(f"Audio saved to {output_path}")

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("ELEVENLABS_API_KEY")
    client = ElevenLabs(api_key=api_key)
    
    description = "A high-pitched sound mingles with the roar, slowly increasing and sounding almost like the roar of an engine."
    
    audio_data = generate_sound_effect(client, description)
    
    save_audio(audio_data, "output.mp3")