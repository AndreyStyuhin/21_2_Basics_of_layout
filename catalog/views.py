from django.shortcuts import render
# 1. Объединяем импорты моделей в одну строку
from catalog.models import Product, Category, ContactInfo


def home(request):
    """Контроллер главной страницы с выводом последних 5 продуктов."""

    # 2. Получаем 5 последних продуктов
    # Мы проверили в Shell, что данные есть. Теперь, когда нет перезаписи, код заработает.
    latest_products = Product.objects.order_by('-created_at')[:5]

    # 3. Выводим в консоль (как в задании)
    print("--- 5 последних продуктов ---")
    for product in latest_products:
        # Проверка, что продукт имеет категорию (мы это уже подтвердили)
        category_name = product.category.name if product.category else 'Нет категории'
        print(f"ID: {product.id}, Name: {product.name}, Category: {category_name}")
    print("----------------------------")

    # 4. Передаем в шаблон
    context = {
        'latest_products': latest_products,
        'title': 'Главная страница'
    }
    return render(request, 'catalog/home.html', context)


def contacts(request):
    """Контроллер страницы контактов с обработкой POST-формы."""

    # Получаем контактную информацию (берем первую запись)
    contact_data = ContactInfo.objects.first()

    context = {
        'contact_data': contact_data,
        'title': 'Контакты'
    }

    if request.method == "POST":
        name = request.POST.get('user_name')
        email = request.POST.get('user_email')
        message = request.POST.get('user_message')

        # Обновленная логика вывода в консоль
        print(f"--- Сообщение с контактов ---")
        print(f"Имя: {name}, Email: {email}")
        print(f"Сообщение: {message}")
        print("----------------------------")

        context.update({
            'success': True,
            'name': name,
        })
        # Остаемся на странице контактов, передавая информацию об успехе
        return render(request, 'catalog/contacts.html', context)

    # Для GET-запроса возвращаем страницу с контактными данными
    return render(request, 'catalog/contacts.html', context)


def category(request):
    """Контроллер страницы категорий"""
    return render(request, 'catalog/category.html')


def orders(request):
    """Контроллер страницы заказов"""
    return render(request, 'catalog/orders.html')