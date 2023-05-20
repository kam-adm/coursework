import logging
import YandexDisk
import VK

logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s"
                    )
TOKEN = input("Введите токен яндекс диска: ")
logging.info('Введён токен яндекс диска.')
ya = YandexDisk.YandexDisk(TOKEN)
vk_token = input("Введите вк токен: ")
id_vk = int(input("Введите id пользователя: "))
quantiti_foto = int(input("Введите колличество фото: "))
logging.info('Введено колличество фото.')
vk = VK.VK(id_vk, vk_token, quantiti_foto)
vk.users_info()
ya.create_folder()
photo_to_upload = vk.vk_foto_sort()
logging.info('Получен список фото для загрузки.')
ya.upload_files(photo_to_upload)
ya.loading_progress_bar(photo_to_upload)
