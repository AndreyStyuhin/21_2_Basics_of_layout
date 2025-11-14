from django.core.management import BaseCommand, call_command
from catalog.models import Product, Category


class Command(BaseCommand):
    """
    Кастомная команда для заполнения базы данных тестовыми данными из фикстуры.
    """

    help = 'Загружает данные из фикстуры catalog/fixtures/data.json'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Очистка базы данных...'))

        # Предварительное удаление данных (Критерий 9)
        # Удаляем Продукты первыми из-за ForeignKey
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('База данных очищена.'))

        try:
            # Загрузка фикстуры (Критерий 9)
            self.stdout.write(self.style.WARNING('Загрузка данных из фикстуры...'))
            call_command('loaddata', 'catalog/fixtures/data.json')
            self.stdout.write(self.style.SUCCESS('Данные успешно загружены.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке данных: {e}'))