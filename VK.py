import logging
import requests
import json

logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s"
                    )
class VK:
   def __init__(self, access_token, user_id, version='5.131'):
       self.token = access_token
       self.id = user_id
       self.version = version
       self.params = {'access_token': self.token, 'v': self.version}

   def users_info(self):
       url = 'https://api.vk.com/method/users.get'
       params = {'user_ids': self.id}
       response = requests.get(url, params={**self.params, **params})
       if response.status_code == 200:
           print('Информация о пользователе загружена!')
           logging.info('Информация о пользователе загружена!')
       else:
           print('Инфоормация о пользователе не загружена.')
           logging.error('Инфоормация о пользователе не загружена.')
       for e in response.json()['response']:
           if e['first_name'] == 'DELETED':
               print('Пользователь удалён!!!')
               logging.error('Пользователь удалён!!! -- DELETED')
               exit()
           return print("Владельцем данного id является: ", e['first_name'], e['last_name'] )


   def vk_foto(self):
       api = requests.get('https://api.vk.com/method/photos.getAll', params={
           'owner_id': self.id,
           'access_token': self.token,
           'foto_sizes': 1,
           'extended': 1,
           'count': 200,
           'v': self.version
       })
       return json.loads(api.text)



access_token = ''
user_id = int(input("Введите id пользователя:"))
logging.info('Введён id пользователя.')
vk = VK(access_token, user_id)
vk.users_info()
