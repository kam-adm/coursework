import logging
import requests
import json
from heapq import nlargest

logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s"
                    )
class VK:
   def __init__(self, user_id, token_vk, quantiti_foto, version='5.131'):
       logging.info('Введён id пользователя.')
       self.token = token_vk
       self.id = user_id
       self.quantiti_foto = quantiti_foto
       self.version = version
       self.params = {'access_token': self.token, 'v': self.version}

   def users_info(self):
       url = 'https://api.vk.com/method/users.get'
       params = {'user_ids': self.id}
       response = requests.get(url, params={**self.params, **params})
       if response.status_code != 200:
           logging.error('Инфоормация о пользователе не загружена.')
           exit()
       elif response.status_code == 200:
           if 'response' not in response.json():
               logging.error("Введён неверный vk token!!!")
               exit()
           if len(response.json()['response']) == 0:
               logging.error("Введён неверный id!!!")
               exit()
           else:
               logging.info('Информация о пользователе загружена!')
               for status_user in response.json()['response']:
                   if status_user['first_name'] == 'DELETED':
                       logging.error('Пользователь удалён!!! -- DELETED')
                       exit()
                   else:
                       logging.info(f"Владельцем данного id является: {status_user['first_name']} {status_user['last_name']}")
                   return

   def vk_foto_serch(self):
       quantiti_foto_serch = self.quantiti_foto
       api = requests.get('https://api.vk.com/method/photos.get', params={
       'owner_id': self.id,
       'access_token': self.token,
       'foto_sizes': 1,
       'extended': 1,
       'count': 200,
       'v': self.version,
       'album_id': 'profile'
         })
       if api.status_code != 200:
            logging.error('Данные не получены, запрос завершился с кодом', api.status_code)
            exit()
       data_acquisition = json.loads(api.text)
       if 'response' not in data_acquisition:
           logging.error('Введенны неверный id или id закрытого профиля!')
           exit()
       elif data_acquisition['response']['count'] == 0:
           logging.info('У данного пользователя нет ни одной фотографии.')
           exit()
       elif data_acquisition['response']['count'] < quantiti_foto_serch:
           logging.info(f"У пользователя в альбоме всего {data_acquisition['response']['count']} фото, это колличество и будет загруженно на яндекс диск!")
       return data_acquisition
   def vk_foto_sort(self):
       foto_serch = self.vk_foto_serch()
       quantiti_foto_sort = self.quantiti_foto
       dict_foto = {}
       list_size = []
       result_foto = {}
       foto_count = 0
       for metadata in foto_serch['response']['items']:
           url_foto = metadata['sizes'][-1]['url']
           likes_quantiti = metadata['likes']['count']
           type_foto = metadata['sizes'][-1]['type']
           size_foto = metadata['sizes'][-1]['height'] + metadata['sizes'][-1]['width']
           dict_foto.update({url_foto: [likes_quantiti, type_foto, size_foto]})
           list_size.append(size_foto)
       for key, value in dict_foto.items():
           for sort_foto in nlargest(quantiti_foto_sort, list_size):
               if sort_foto in value:
                   result_foto.update({key: [value]})
                   foto_count += 1
           if quantiti_foto_sort <= len(result_foto.values()):
               break
       return result_foto
