from config import api, base_url
import requests
from abc import ABC, abstractmethod
import datetime


class Weather(ABC):
    @abstractmethod
    def __init__(self):
        self.url = base_url
        self.api = api

    @abstractmethod
    def Weather_City(self, data='', city=''):
        pass


class City_day(Weather, ABC):
    def __init__(self):
        super().__init__()

    def Datetime(self, data):
        if data is None or data.lower() == 'сегодня':
            data = [datetime.datetime.now().strftime("%Y-%m-%d")]
        elif data.lower() == 'завтра':
            data = datetime.datetime.now().strftime("%Y-%m-%d")
            data = data.split('-')
            data = ['-'.join([data[0], data[1], str(int(data[2]) + 1)])]
        elif data.lower() == 'послезавтра':
            data = datetime.datetime.now().strftime("%Y-%m-%d")
            data = data.split('-')
            data = ['-'.join([data[0], data[1], str(int(data[2]) + 2)])]
        else:
            list_data = []
            for i in range(0, int(data)):
                dt = datetime.datetime.now().strftime("%Y-%m-%d")
                dt = dt.split('-')
                list_data.append('-'.join([dt[0], dt[1], str(int(dt[2]) + i)]))
            data = list_data

        return data

    def Weather_City(self, data=None, city=''):
        data = City_day().Datetime(data)

        city = f"{city},RU"

        try:
            req = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                               params={'q': city, 'type': 'like', 'units': 'metric', 'APPID': self.api})
            date = req.json()
            list_dict_date_weather = []
            for i in data:
                dict_weather_city = {'Время': set(), 'Температура': [], 'Давление': [], 'Влажность': [], 'Небо': set()}
                for j in date['list']:
                    if j['dt_txt'].split()[0] == i:
                        dict_weather_city['Время'].add(j['dt_txt'].split()[0])
                        dict_weather_city['Температура'].append(float('{0:+3.0f}'.format(j['main']['temp'])))
                        dict_weather_city['Небо'].add(j['weather'][0]['description'])
                        dict_weather_city['Давление'].append(float(j['main']['pressure']))
                        dict_weather_city['Влажность'].append(float(j['main']['humidity']))
                list_dict_date_weather.append(dict_weather_city)
            return list_dict_date_weather
        except:
            return 'Упс, ошибка, вы ввели неверные данные'
