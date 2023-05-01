import requests
import json
import logging
from YandexDisk import ya
from VK import vk
import time
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s"
                    )
vk.users_info()
list_json = []
ya.create_folder()
print("Получен список фото для загрузки.")
logging.info('Получен список фото для загрузки.')
for key, value in vk.vk_foto_serch_and_sort().items():
    logging.info(f'Получена ссылка на загрузку изображения: {key}')
    r = requests.get(url=key)
    list_json.append([{"file_name": f'{value[0][0]}.jpg', "size": value[0][1]}])
    with open('data.json', 'w') as o:
        json.dump(list_json, o)
    ya.upload_file_to_disk(f'{key}', f'vk_backup_foto/{value[0][0]}.jpg')
    logging.info(f'Изображению присвоено имя {value[0][0]}.jpg и оно успешно загружено на яндекс диск!')
    for progress_bar in tqdm(list_json):
        time.sleep(0.2)
print("Все изображения успешно загружены на яндекс диск!")
logging.info('Все изображения успешно загружены на яндекс диск!')
