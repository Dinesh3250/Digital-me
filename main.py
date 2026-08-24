import os
from dotenv import load_dotenv
from openai import Openai


load_dotenv(override=True)
openai = Openai()
openai_api_key = os.getenv("OPENAI_API_KEY")

pushover_user = os.getenv("PUSHOVER_USER")
pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_url = os.getenv("PUSHOVER_URL", "https://api.pushover.net/1/messages.json")


def main():
    print("Hello from digital-me!")


if __name__ == "__main__":
    main()
