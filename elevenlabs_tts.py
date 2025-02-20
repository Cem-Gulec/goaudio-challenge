import os
from dotenv import load_dotenv

def main():
    # Initialize the client
    load_dotenv()
    api_key = os.getenv("ELEVENLABS_API_KEY")

if __name__ == "__main__":
    main()