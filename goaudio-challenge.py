from pathlib import Path
from openai import OpenAI

# initialize the OpenAI API client
api_key = ""
client = OpenAI(api_key=api_key)

# sample text to generate speech from
text = """In his miracle year, he published four groundbreaking papers. 
These outlined the theory of the photoelectric effect, explained Brownian motion, 
introduced special relativity, and demonstrated mass-energy equivalence."""

response = client.audio.speech.create(
    model="tts-1",
    voice="nova",
    input=text,
    speed=1.0,
)

# save the generated speech using the streaming response method
with open("openai-output.mp3", "wb") as file:
    for chunk in response.iter_bytes():
        file.write(chunk)