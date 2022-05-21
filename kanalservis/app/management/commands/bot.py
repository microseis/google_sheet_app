from django.core.management.base import BaseCommand
from django.conf import settings
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from ...models import Order
from channels.db import database_sync_to_async

from datetime import date

today = date.today()


class Command(BaseCommand):
    """ Функционал проверки соблюдения «срока поставки» из таблицы.
    В случае, если срок прошел, скрипт отправляет уведомление в Telegram"""
    help = "Telegram Bot"

    def handle(self, *args, **options):
        bot = Bot(token=settings.TOKEN)
        dp = Dispatcher(bot)

        @dp.message_handler(commands=['start'])
        async def send_welcome(message: types.Message):
            to_deliver = await get_data()
            #print(len(to_deliver))
            for i in range(0, len(to_deliver)):
                await message.answer(
                    f'✅ Заказ с истекшим сроком поставки на дату {today.strftime("%d/%m/%Y")}:\n\n'
                    f' {to_deliver[i].ord_num}')

        async def scheduled(wait_for):
            while True:
                await asyncio.sleep(wait_for)
                to_deliver = await get_data()

                for i in range(0, len(to_deliver)):
                    await bot.send_message(365093091,
                        f'✅ Заказ с истекшим сроком поставки на дату {today.strftime("%d/%m/%Y")}:\n\n'
                        f' {to_deliver[i].ord_num}')

        @database_sync_to_async
        def get_data():
            orders = Order.objects.filter(ord_date=today)
            print(len(orders))
            return orders

        loop = asyncio.get_event_loop()
        loop.create_task(scheduled(30)) # 86400
        executor.start_polling(dp, skip_updates=True)
