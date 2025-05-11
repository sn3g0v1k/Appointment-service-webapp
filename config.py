import os

from dotenv import load_dotenv

from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, '.env'))



BOT_TOKEN = os.getenv('BOT_TOKEN')
CP_TOKEN = os.getenv('CP_TOKEN')

if not CP_TOKEN:

    raise ValueError("CP_TOKEN not found in .env")

if not CP_TOKEN:

    raise ValueError("CP_TOKEN not found in .env")

