## Description of The Project

We just concluded a meeting with a publisher who is interested in creating an audio drama (Hörspiel) with us. To get a sense of the possibilities, they would like to get a demo and have provided us with a script for this purpose. They are looking for a 1-minute audio sample showcasing what the final audio drama could sound like and would also like to understand the process behind it. We need to keep in mind that this needs to build a scalable solution in the long-term.

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

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



### Installation

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
   git clone https://github.com/github_username/repo_name.git
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
