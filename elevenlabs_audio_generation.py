from dotenv import load_dotenv
import os
from elevenlabs.client import ElevenLabs

load_dotenv()
api_key = os.getenv("ELEVENLABS_API_KEY")

elevenlabs = ElevenLabs(api_key=api_key)


def generate_sound_effect(text: str, output_path: str):
    print("Generating sound effects...")

    result = elevenlabs.text_to_sound_effects.convert(
        text=text,
        duration_seconds=10,  # Optional
        prompt_influence=0.3,  # Optional
    )

    with open(output_path, "wb") as f:
        for chunk in result:
            f.write(chunk)

    print(f"Audio saved to {output_path}")


if __name__ == "__main__":
    description = "A high-pitched sound mingles with the roar, slowly increasing and sounding almost like the roar of an engine."
    generate_sound_effect(description, "output.mp3")