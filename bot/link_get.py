import requests
from config import IMGBB_API_KEY
import base64



def rehost_image(image_url):
    # Скачиваем изображение

    response = requests.get(image_url)

    if response.status_code != 200:
        raise Exception("Не удалось скачать изображение")

    # Кодируем в base64

    image_base64 = base64.b64encode(response.content).decode('utf-8')

    # Отправляем на imgbb

    upload_url = "https://api.imgbb.com/1/upload"

    payload = {

        "key": IMGBB_API_KEY,

        "image": image_base64,

    }

    upload_response = requests.post(upload_url, data=payload)

    result = upload_response.json()

    if result.get("success"):

        return result["data"]["url"]  # Готовая ссылка на изображение

    else:

        raise Exception("Ошибка при загрузке на imgbb", result)


# Пример использования

# original_url = "https://api.telegram.org/file/bot7752395409:AAERIXF8H8DqDeTCGnTT7qxXupEvZgd9ULU/photos/file_4.jpg"
#
# hosted_url = rehost_image(original_url)
#
# print("Картинка теперь по адресу:", hosted_url)
