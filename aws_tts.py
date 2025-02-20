import os
import boto3
from dotenv import load_dotenv

load_dotenv()

polly_client = boto3.Session(
    aws_access_key_id=os.getenv("aws_access_key_id"),                     
    aws_secret_access_key=os.getenv("aws_secret_access_key"),
    region_name='us-west-2').client('polly')

response = polly_client.synthesize_speech(VoiceId='Joanna',
                OutputFormat='mp3', 
                Text = 'This is a sample text to be synthesized.',
                Engine = 'neural')

file = open('speech.mp3', 'wb')
file.write(response['AudioStream'].read())
file.close()