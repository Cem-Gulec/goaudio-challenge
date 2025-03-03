import os
from dotenv import load_dotenv
import boto3

load_dotenv()

polly_client = boto3.Session(
        aws_access_key_id=os.getenv("aws_access_key_id"),
        aws_secret_access_key=os.getenv("aws_secret_access_key"),
        region_name='us-east-1'
    ).client('polly')

# SSML text with whispering effect
ssml_text = """
<speak>
    <amazon:effect name="whispered">Leo… Was hast du getan?</amazon:effect>
</speak>
"""

# Convert text to speech
response = polly_client.synthesize_speech(
    Text=ssml_text,
    TextType="ssml",
    VoiceId="Matthew",
    OutputFormat="mp3",
    LanguageCode='de-DE'
)

# Save the audio file
audio_file = "whisper_output.mp3"
with open(audio_file, "wb") as f:
    f.write(response["AudioStream"].read())

print(f"Whispering speech saved as {audio_file}")