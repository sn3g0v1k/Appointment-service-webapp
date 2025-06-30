import requests
from icecream import ic
from link_get import rehost_image

def profile_photo(file_id, bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}"
    ic(url)
    r = requests.get(url).json()
    path = r["result"]["file_path"]
    ic(f"https://api.telegram.org/file/bot{bot_token}/{path}")
    link = rehost_image(f"https://api.telegram.org/file/bot{bot_token}/{path}")
    return link