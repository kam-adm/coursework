import logging
import requests
import json
from heapq import nlargest

logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s"
                    )

class VK:
   def __init__(self, user_id=int(input('Введите id пользователя: ')), version='5.131'):
       logging.info('Введён id пользователя.')
       self.token = ''
       self.id = user_id
       self.version = version
       self.params = {'access_token': self.token, 'v': self.version}

   def users_info(self):
       url = 'https://api.vk.com/method/users.get'
       params = {'user_ids': self.id}
       response = requests.get(url, params={**self.params, **params})
       if response.status_code != 200:
           print('Инфоормация о пользователе не загружена.')
           logging.error('Инфоормация о пользователе не загружена.')
           exit()
       elif response.status_code == 200:
           if len(response.json()['response']) == 0:
               print("Введён неверный id!!!")
               exit()
           else:
               print('Информация о пользователе загружена!')
               logging.info('Информация о пользователе загружена!')
               for status_user in response.json()['response']:
                   if status_user['first_name'] == 'DELETED':
                       print('Пользователь удалён!!!')
                       logging.error('Пользователь удалён!!! -- DELETED')
                       exit()
                   return print("Владельцем данного id является: ", status_user['first_name'], status_user['last_name'])


   def vk_foto(self):
       api = requests.get('https://api.vk.com/method/photos.get', params={
           'owner_id': self.id,
           'access_token': self.token,
           'foto_sizes': 1,
           'extended': 1,
           'count': 200,
           'v': self.version,
           'album_id': 'profile'
       })
       print(api.json())
       if api.status_code != 200:
           print('Данные не получены, запрос завершился с кодом', api.status_code)
           exit()
       print(api.status_code)
       return json.loads(api.text)
   def vk_check(self):
       if vk.vk_foto()['response']['count'] == 0:
           print("У пользователя нет фото!")
           logging.error("У пользователя нет фото!")
           exit()
       if len(vk.vk_foto()['response']['items']) == 0:
            print("В ответе от сервера нет необходимых данных")
            logging.error("В ответе от сервера нет необходимых данных")
            exit()
       for metadata in vk.vk_foto()['response']['items']:
           if len(metadata['sizes'][-1]['url']) == 0 and len(metadata['sizes'][-1]['type']) == 0 and len(metadata['sizes'][-1]['height']) == 0 and len(metadata['sizes'][-1]['width']) == 0:
               print("В ответе от сервера нет необходимых данных")
               logging.error("В ответе от сервера нет необходимых данных")
               exit()

   def vk_foto_serch_and_sort(self, quantiti_foto=int(input("Введите колличество фото: "))):
       vk.vk_check()
       logging.info("Произведена проверка данных.")
       logging.info('Введено колличество фото.')
       dict_foto = {}
       list_size = []
       result_foto = {}
       if vk.vk_foto()['response']['count'] < quantiti_foto:
           print(f"У пользователя в альбоме всего {vk.vk_foto()['response']['count']} фото, это колличество и будет загруженно на яндекс диск!")
       for metadata in vk.vk_foto()['response']['items']:
           url_foto = metadata['sizes'][-1]['url']
           likes_quantiti = metadata['likes']['count']
           type_foto = metadata['sizes'][-1]['type']
           size_foto = metadata['sizes'][-1]['height'] + metadata['sizes'][-1]['width']
           dict_foto.update({url_foto: [likes_quantiti, type_foto, size_foto]})
           list_size.append(size_foto)
       for key, value in dict_foto.items():
           for sort_foto in nlargest(quantiti_foto, list_size):
               foto_count = 0
               if sort_foto in value:
                   result_foto.update({key: [value]})
                   foto_count += 1
           if quantiti_foto <= len(result_foto.values()):
               break
       return result_foto
vk = VK()
