import requests
import json
import logging
import time
from tqdm import tqdm
logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
                     format="%(asctime)s %(levelname)s %(message)s"
                     )

class YandexDisk:
    def __init__(self, token):
        self.token = token
    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }
    def get_files_list(self):
        file_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        headers = self.get_headers()
        response = requests.get(file_url, headers=headers)
        return response.json()

    def create_folder(self, path='vk_backup_foto'):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {"overwrite": "true"}
        requests.put(f'{url}?path={path}', headers=headers, params=params)

    def get_upload_link(self, disk_file_path):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        data = response.json()
        href = data.get('href')
        return href

    def upload_file_to_disk (self, url, disk_file_path):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {"url": url, "path": disk_file_path, "overwrite": "true"}
        response = requests.post(upload_url, headers=headers, params=params)
        if response.status_code != 202:
            logging.error(f'Изображение не загружено, код ошибки:{response.status_code} (Проверьте правильность ввода ключа яндекс диска!)')
            exit()
    def upload_files(self, foto_sort):
        json_list_of_uploaded_photos = []
        for key, value in tqdm(foto_sort.items()):
            time.sleep(0.2)
            logging.info(f'Получена ссылка на загрузку изображения: {key}')
            self.upload_file_to_disk(f'{key}', f'vk_backup_foto/{value[0][0]}.jpg')
            logging.info(f'Изображению присвоено имя {value[0][0]}.jpg и оно успешно загружено на яндекс диск!')
            json_list_of_uploaded_photos.append([{"file_name": f'{value[0][0]}.jpg', "size": value[0][1]}])
            with open('data.json', 'w') as o:
                json.dump(json_list_of_uploaded_photos, o)
        logging.info('Все изображения успешно загружены на яндекс диск!')
