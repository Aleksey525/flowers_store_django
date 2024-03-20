from django.core.management.base import BaseCommand
from flowers_store.apps.bot.main_bot import bot


class Command(BaseCommand):
    help = "Запускаем бота"


    def handle(self, *args, **options):
        bot.infinity_polling()


