import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply('Привет! Где смотрим погоду?')


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_icons = {
        'Clear': 'Ясно \U00002600',
        'Rain': 'Дождь \U00002614',
        'Clouds': 'Облачно \U00002601',
        'Drizzle': 'Дождь \U00002614',
        'Snow': 'Снег \U00002744',
        'Mist': 'Туман \U0001F32B',
        'Thunderstorm': 'Гроза \U0001F329',
    }
    try:
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric'
        )
        data = r.json()

        city = data['name']
        description = data['weather'][0]['main']

        if description in code_to_icons:
            wd = code_to_icons[description]
        else:
            wd = 'Непонятно, посмотрите в окно!'
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        feels_like = data['main']['feels_like']
        sunrise_time = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_time = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        lenght_day = datetime.datetime.fromtimestamp(data['sys']['sunset']) - datetime.datetime.fromtimestamp(
            data['sys']['sunrise'])

        await message.reply(f'*** {datetime.datetime.now().strftime("%d-%m-%Y %H:%M")} ***\n'
                            f'Погода в городе: {city}\n'
                            f'{wd}\n'
                            f'Температура: {temp} °C\n'
                            f'Влажность: {humidity} %\n'
                            f'Ветер: {wind} м/c\n'
                            f'Ощущается как: {feels_like} °C\n'
                            f'Время рассвета: {sunrise_time.strftime("%d-%m-%Y %H:%M")}\n'
                            f'Время заката: {sunset_time.strftime("%d-%m-%Y %H:%M")}\n'
                            f'Продолжительность дня: {lenght_day}\n'
                            )

    except:

        await message.reply('Проверьте название города!')


if __name__ == '__main__':
    executor.start_polling(dp)
