import boto3

# Initialize Amazon Polly client
polly_client = boto3.client("polly", region_name="us-east-1")  # Change region if needed

# SSML text with whispering effect
ssml_text = """
<speak>
    <amazon:effect name="whispered">This is a whisper. Can you hear me?</amazon:effect>
</speak>
"""

# Convert text to speech
response = polly_client.synthesize_speech(
    Text=ssml_text,
    TextType="ssml",
    VoiceId="Matthew",  # "Matthew" supports whispering
    OutputFormat="mp3"
)

# Save the audio file
audio_file = "whisper_output.mp3"
with open(audio_file, "wb") as f:
    f.write(response["AudioStream"].read())

print(f"Whispering speech saved as {audio_file}")