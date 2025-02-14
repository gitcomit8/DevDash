from dotenv import load_dotenv
load_dotenv()
import os

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

if not GITHUB_CLIENT_ID or not GITHUB_CLIENT_SECRET:
    raise Exception("GITHUB_CLIENT_ID or GITHUB_CLIENT_SECRET is not set. Check your .env file.")
