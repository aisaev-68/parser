from django.core.management.base import BaseCommand
import asyncio
from rate.parser import run_parser


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write("Парсинг сайта МТС.")
        run_parser()
        self.stdout.write("Завершение работы парсера.")