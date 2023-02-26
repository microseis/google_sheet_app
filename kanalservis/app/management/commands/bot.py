import asyncio
from datetime import date
import os

from aiogram import Bot, Dispatcher, executor, types
from channels.db import database_sync_to_async
from django.conf import settings
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from asgiref.sync import sync_to_async

from ...models import Order

load_dotenv()

today = date.today()
ADMIN_ID = os.environ.get("ADMIN")


class Command(BaseCommand):
    """Функционал проверки соблюдения «срока поставки» из таблицы.
    В случае, если срок прошел, скрипт отправляет уведомление в Telegram"""

    help = "Telegram Bot"

    def handle(self, *args, **options):
        bot = Bot(token=settings.TOKEN)
        dp = Dispatcher(bot)

        @database_sync_to_async
        def get_data() -> list:
            orders = Order.objects.filter(ord_date=today)
            return list(orders)

        @dp.message_handler(commands=["start"])
        async def send_welcome(message: types.Message):
            to_deliver = await get_data()
            print(to_deliver)
            for i in range(0, len(to_deliver)):
                await message.answer(
                    f'✅ Заказ с истекшим сроком поставки на дату {today.strftime("%d/%m/%Y")}:\n\n'
                    f" {to_deliver[i].ord_num}"
                )

        async def scheduled(wait_for):
            while True:
                await asyncio.sleep(wait_for)

                to_deliver = await get_data()

                for i in range(0, len(to_deliver)):
                    await bot.send_message(
                        ADMIN_ID,
                        f'✅ Заказ с истекшим сроком поставки на дату {today.strftime("%d/%m/%Y")}:\n\n'
                        f" {to_deliver[i].ord_num}",
                    )

        loop = asyncio.get_event_loop()
        loop.create_task(scheduled(30))  # 86400
        executor.start_polling(dp, skip_updates=True)
