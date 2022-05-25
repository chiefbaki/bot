import requests

# Сторонние библиотеки
import vk_api
from bs4 import BeautifulSoup
from vk_api import VkUpload
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from PIL import Image, ImageDraw, ImageFont
from urllib.request import urlopen


class Weather:
    def __init__(self) -> None:
        """
        Конструктор
        """
        self.vk_session = vk_api.VkApi(token='6b36926d25a772b75c0d608cd7c272521630175dabe9518bc55bfc1a1487aa988537e980df5e27bbc0be3')
        self.vk = self.vk_session.get_api()
        self.longpoll = VkLongPoll(self.vk_session)

    def weather_tomorrow(self, user_id):
        upload = VkUpload(self.vk_session)
        attachments = []
        image = Image.open('weather_pattern.jpg')
        # img = image.resize((400, 500))
        img = image.resize((400, 260))
        img = img.convert('RGB')
        idraw = ImageDraw.Draw(img)
        title = ImageFont.truetype(font='lato.ttf', size=30)
        font = ImageFont.truetype(font='lato.ttf', size=18)
        # title2 = ImageFont.truetype(size=30)
        idraw.text((10, 10), 'Погода в Москве', font=title, fill="white")
        response = requests.get("http://api.openweathermap.org/data/2.5/weather",
                                params={'q': 'moscow,ru', 'units': 'metric', 'APPID': '3051c8da538a2e104685783dae4796f4',
                                        'lang': 'ru'})
        info = response.json()
        img_name = info['weather'][0]['icon']
        im = Image.open(urlopen('https://openweathermap.org/img/wn/{}@4x.png'.format(img_name)))
        img.paste(im, (95, 20), im.convert('RGBA'))
        status = info['weather'][0]['description'].capitalize()
        temp = str(int(info['main']['temp_min'])) + ' - ' + str(int(info['main']['temp_max']))
        pressure = str(int(float(info['main']['pressure']) / 1.33))
        humidity = str(info['main']['humidity'])
        wind_speed = info['wind']['speed']
        wind_slug = self._get_wind_slug(float(wind_speed)).lower()
        wind_deg_slug = self._get_wind_deg_slug(info['wind']['speed'])
        weather = '{}, температура: {}°C\nДавление: {} мм рт. сб., влажность: {}%\nВетер: {}, {} м/с, {}'.format(status,
                                                                                                                 temp,
                                                                                                                 pressure,
                                                                                                                 humidity,
                                                                                                                 wind_slug,
                                                                                                                 wind_speed,
                                                                                                                 wind_deg_slug)
        idraw.text((10, 185), weather, font=font, fill="white")
        img.save('data/weather_card.png')

        photo = upload.photo_messages('data/weather_card.png')[0]

        attachments.append("photo{}_{}".format(photo["owner_id"], photo["id"]))

        self._send_message_with_attachments(user_id=user_id, text='Сейчас', attachments=attachments)


