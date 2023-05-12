import logging
import YandexDisk
import VK
import time
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s"
                    )
TOKEN = input("Введите токен яндекс диска: ")
logging.info('Введён токен яндекс диска.')
ya = YandexDisk.YandexDisk(TOKEN)
vk_token = input("Введите вк токен: ")
id_vk = int(input("Введите id пользователя: "))
quantiti_foto = int(input("Введите колличество фото: "))
vk = VK.VK(id_vk, vk_token)
vk.users_info()
list_json = []
ya.create_folder()
logging.info('Получен список фото для загрузки.')
for key, value in vk.vk_foto_serch_and_sort(quantiti_foto).items():
    vk.list_foto_json(key, value, list_json)
    logging.info(f'Получена ссылка на загрузку изображения: {key}')
    ya.upload_file_to_disk(f'{key}', f'vk_backup_foto/{value[0][0]}.jpg')
    logging.info(f'Изображению присвоено имя {value[0][0]}.jpg и оно успешно загружено на яндекс диск!')
    for progress_bar in tqdm(list_json):
        time.sleep(0.2)
logging.info('Все изображения успешно загружены на яндекс диск!')