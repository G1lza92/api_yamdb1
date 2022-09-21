from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Загружает тестовые данные в db.sqlite3'

    def add_arguments(self, parser):
        parser.add_argument('table_names', nargs='*', type=str)

    def handle(self, *args, **options):
        for table_name in options['table_names']:
            try:
                ...
            except Exception as error:
                raise CommandError(
                    f'При загрузке таблицы {table_name} произошла ошибка.'
                    f'\r\n{error}'
                )
            self.stdout.write(self.style.SUCCESS(f'{table_name}'))
