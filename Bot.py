import telebot, config
from numpy import mean
from Weather.Request import City_day

city = City_day()
bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def Welcome(message):
    bot.send_message(message.chat.id, "Привет, меня зовут Жорик, и  бот прогноза погоды. "
                                      "Если тебе нужна инструкция, то вызови /help")


@bot.message_handler(commands=['help'])
def Helps(message):
    bot.send_message(message.chat.id, """Важная на информация по запросу:\n
    1. Если вы хотите получить прогноз погоды на сегодня, то напишите такой запрос: /day Волгоград или /day Волгоград сегодня.
    2. Если вы хотите получить прогноз погоды на завтра или послезавтра, то напишите такой запрос: /day Волгоград завтра или /day Волгоград послезавтра.
    3. Если вы хотите получить прогноз погоды на несколько дней, то напишите такой запрос: /day Волгоград 5 (Показывает прогноз на 5 дней включая сегодня).""")


@bot.message_handler(commands=['day'])
def City(message):
    if len(message.text.split()) >= 2:
        if len(message.text.split()) == 2:
            weather = city.Weather_City(city=message.text.split()[1])
        elif len(message.text.split()) == 3:
            weather = city.Weather_City(city=message.text.split()[1], data=message.text.split()[2])

        if type(weather) == str:
            bot.send_message(message.chat.id, weather)
        else:
            for dict_weather in weather:
                string = "Прогноз на выбранные дни/день: \n" + '\n'.join([
                    'Время: ' + ', '.join(dict_weather['Время']),
                    'Температура: ' + str(round(mean(dict_weather['Температура']))),
                    'Давление: ' + str(round(mean(dict_weather['Давление']))),
                    'Влажность: ' + str(round(mean(dict_weather['Влажность']))),
                    'Небо: ' + ', '.join(dict_weather['Небо'])
                ])
                bot.send_message(message.chat.id, string)
    else:
        bot.send_message(message.chat.id, "Упс, ошбка введите ещё раз(")


if __name__ == '__main__':
    bot.polling(none_stop=True)
