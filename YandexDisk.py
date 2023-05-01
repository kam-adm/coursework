import requests
import logging


logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
                     format="%(asctime)s %(levelname)s %(message)s"
                     )

TOKEN = input("Введите токен яндекс диска: ")
logging.info('Введён токен яндекс диска.')


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
        print(response.json())
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
        if response.status_code == 200:
            print('Ключ яндекс диска успешно проверен!')
            logging.info('Ключ яндекс диска успешно проверен!')
        else:
            print('При проверке ключа яндекс диска произошла ошибка: ', response.status_code)
            logging.error(f'При проверке ключа яндекс диска произошла ошибка: {response.status_code}')
            print('Проверьте правильность ввода ключа и повторите попытку.')
            exit()
        data = response.json()
        href = data.get('href')
        return href

    def upload_file_to_disk(self, url, disk_file_path):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {"url": url, "path": disk_file_path, "overwrite": "true"}
        response = requests.post(upload_url, headers=headers, params=params)
        if response.status_code != 202:
            print('Изображение не загружено, код ошибки:', response.status_code)
            exit()
ya = YandexDisk(token=TOKEN)
