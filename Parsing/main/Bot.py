import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from aiogram.dispatcher.filters import Text
from config import token
from main import check_news_update


bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)



@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Все новости", "Последние 3 новости", "Свежие новости"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Лента новостей", reply_markup=keyboard)


@dp.message_handler(Text(equals="Все новости"))
async def get_all_news(message: types.Message):
    with open("news_dict.json", encoding='utf8') as file:
        news_dict = json.load(file)
    
    for k, v in sorted(news_dict.items()):
        news = f"{hbold(v['bbc_date_time'])}\n" \
               f"{hlink(v['bbc_title'], v['bbc_url'])}"
               #f"{hunderline(v['bbc_title'])}\n" \
               #f"{hcode(v['bbc_desc'])}\n" \
        await message.answer(news)


@dp.message_handler(Text(equals="Последние 3 новости"))
async def get_last_five_news(message: types.Message):
    with open("news_dict.json", encoding='utf8') as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-3:]:
        news = f"{hbold(v['bbc_date_time'])}\n" \
               f"{hlink(v['bbc_title'], v['bbc_url'])}"
        await message.answer(news)


@dp.message_handler(Text(equals="Свежие новости"))
async def get_fresh_news(message: types.Message):
    fresh_news = check_news_update()

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            news = f"{hbold(v['bbc_date_time'])}\n" \
                   f"{hlink(v['bbc_title'], v['bbc_url'])}"

            await message.answer(news)

    else:
        await message.answer("Пока нет свежих новостей...")







if __name__ == '__main__':
    #loop = asyncio.get_event_loop()
    #loop.create_task(news_every_minute())
    executor.start_polling(dp)