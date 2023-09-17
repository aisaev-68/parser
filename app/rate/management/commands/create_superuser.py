from decouple import config
from django.core.management.base import BaseCommand

from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):

        self.stdout.write("Создание суперпользователя")

        username = config('USERNAME')
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=config('EMAIL'),
                password=config('PASSWORD'),
                last_name=config('LAST_NAME'),
                first_name=config('FIRST_NAME'),
            )
            self.stdout.write("Суперпользователь создан")
        else:
            self.stdout.write("Суперпользователь уже существует")
