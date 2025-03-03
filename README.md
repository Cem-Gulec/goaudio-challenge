## Description of The Project

We just concluded a meeting with a publisher who is interested in creating an audio drama (Hörspiel) with us. To get a sense of the possibilities, they would like to get a demo and have provided us with a script for this purpose. They are looking for a 1-minute audio sample showcasing what the final audio drama could sound like and would also like to understand the process behind it. We need to keep in mind that this needs to build a scalable solution in the long-term.

## Folder Structure
- **root/**
  - **code/**
    - elevenlabs_tts.py: Main script for generating all the steps required for the task.
    - elevenlabs_audio_generation.py: Standalone script for audio generation with the Elevenlabs model.
    - file_parser.py: Initial parser script for getting a tabular data out of the .docx file.
    - whispering.py: Script used for only creating whispering dialogues with AWS Polly model.
    - aws_tts.py: Main experimentation script for the AWS Polly model.
    - meta_audio_generation.py: Standalone script for background noise generation with Meta Audiocraft model.
    - openai_tts.py: Main experimentation script for the OpenAI model.
  - **docs/**
    - presentation.pptx
  - **outputs/**
    - combined_dialogue.mp3: The main audio output generated with Elevenlabs that combines each of the audio segments, ranging from environment descriptions to dialogues and everything.
    - openai_output.mp3: This was the first model I tried before switching to the AWS Polly model. For this particular output, I only applied a particular portion of the text to give an intuition in the presentation.
    - aws_output.mp3: This was the second model I used before switching to Elevenlabs completely. Similarly to the OpenAI model, I generated a particular portion of text just to give a reference in the presentation.
    - whisper_output.mp3: This was the output of the AWS Polly model I used when the Elevenlabs did not function well with whispering capabilities.
    - 0.wav: This was the output of the Meta Audiocraft model I used when comparing the generation of background audios. 
  - .gitignore
  - requirements.txt
  - README.md



## Prerequisites

<table>
  <tr>
    <td>

| Requirements      | Version |
|-------------------|---------|
| deep-translator   | 1.11.4  |
| elevenlabs        | 1.51.0  |
| pydub             | 0.25.1  |
| python-docx       | 1.1.2   |
| python-dotenv     | 1.0.1   |

</td>
    <td>

| Optional Requirements     | Version |
|---------------------------|---------|
| audiocraft                | 1.3.0   | 
| boto3                     | 1.36.24 |
| botocore                  | 1.36.24 |
| openai                    | 1.63.0  |
| torchaudio                | 2.1.0   |

</td>
  </tr>
</table>



## Installation

1. Create an .env file with the following content
   ```sh
   ELEVENLABS_API_KEY=<KEY>

   # for the optional ones
   OPENAI_API_KEY=<KEY>
   aws_access_key_id=<KEY>
   aws_secret_access_key=<KEY>
   ```
2. Clone the repository
   ```sh
   git clone https://github.com/Cem-Gulec/goaudio-challenge.git
   ```
3. Install dependencies<br><br>
  Mandatory packages:
   ```sh
   pip install -r requirements.txt
   ```

   Optional packages:
   ```sh
   pip install -r requirements.txt[audio]
   pip install -r requirements.txt[aws]
   pip install -r requirements.txt[openai]
   ```
