import csv

from django.core.management.base import BaseCommand, CommandError

from reviews.models import Category, Comment, Genre, Review, Title, User

TABLES = (
    (User, 'users.csv'),
    (Category, 'category.csv'),
    (Genre, 'genre.csv'),
    (Title, 'titles.csv'),
    (Title.genre.through, 'genre_title.csv'),
    (Review, 'review.csv'),
    (Comment, 'comments.csv'),
)


class Command(BaseCommand):
    help = 'Загружает тестовые данные (./static/data/*.csv) в db.sqlite3'

    def handle(self, *args, **options):
        verbosity = int(options['verbosity'])
        for model, file_name in TABLES:
            file_path = './static/data/' + file_name
            try:
                with open(file_path, 'rt', encoding='utf-8') as csv_file:
                    reader = csv.reader(csv_file, delimiter=',', quotechar='"')
                    header = next(reader)
                    model.objects.all().delete()
                    bulk_objs = []
                    for row in reader:
                        kwargs = {
                            key: value for key, value in zip(header, row)
                        }
                        if verbosity > 1:
                            self.stdout.write(str(kwargs))
                        bulk_objs.append(model(**kwargs))
                    model.objects.bulk_create(bulk_objs)
                    if verbosity > 0:
                        self.stdout.write(
                            self.style.SUCCESS(f'{file_name} - done')
                        )
            except Exception as error:
                raise CommandError(
                    f'При загрузке файла {file_name} произошла ошибка.'
                    f'\r\n{error}'
                )
