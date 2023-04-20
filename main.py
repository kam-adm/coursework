import requests
import json
import os
import logging
from YandexDisk import ya
from VK import vk
from heapq import nlargest

logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s"
                    )

def vk_foto_serch():
    for i in vk.vk_foto()['response']['items']:
        k = i['sizes'][-1]['url']
        v = i['likes']['count']
        t = i['sizes'][-1]['type']
        hw = i['sizes'][-1]['height'] + i['sizes'][-1]['width']
        if t == 'z':
            dict_foto.update({k: [v, t, hw]})
            list_hw.append(hw)


def vk_foto_sort():
    count_foto = int(input('Введите колличество фото: '))
    logging.info('Введено колличество фото.')
    for key, value in dict_foto.items():
        for nj in nlargest(count_foto, list_hw):
            if nj in value:
                result_foto.update({key: [value]})




dict_foto = {}
list_hw = []
result_foto = {}
vk_foto_serch()
vk_foto_sort()
list_json = []
ya.create_folder()
print("Получен список фото для загрузки.")
logging.info('Получен список фото для загрузки.')
if not os.path.exists('images'):
    os.mkdir('images')
    print('Локальная папка для загрузки фото создана.')
    logging.info('Локальная папка для загрузки фото создана.')
for key, value in result_foto.items():
    print(f'Получена ссылка на загрузку изображения: {key}')
    logging.info(f'Получена ссылка на загрузку изображения: {key}')
    r = requests.get(url=key)
    list_json.append([{"file_name": f'{value[0][0]}.jpg', "size": value[0][1]}])
    with open(f'images/{value[0][0]}.jpg', 'wb') as f:
        s = f.write(r.content)
        print("Изображение загружено из вк в папку images.")
        logging.info('Изображение загружено из вк в папку images.')
        with open('data.json', 'w') as o:
            json.dump(list_json, o)

    ya.upload_file_to_disk(f'vk_backup_foto/{value[0][0]}.jpg', f'images/{value[0][0]}.jpg')
    print(f'Изображению присвоено имя {value[0][0]}.jpg и оно успешно загружено на яндекс диск!')
    logging.info(f'Изображению присвоено имя {value[0][0]}.jpg и оно успешно загружено на яндекс диск!')
print("\nВсе изображения успешно загружены на яндекс диск!")
logging.info('Все изображения успешно загружены на яндекс диск!')