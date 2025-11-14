from django.shortcuts import render
from .models import Product # 1. Импортируем Product


def home(request):
    # 2. Получаем 5 последних продуктов
    latest_products = Product.objects.order_by('-created_at')[:5]

    # 3. Выводим в консоль (как в задании)
    print("--- 5 последних продуктов ---")
    for product in latest_products:
        print(f"ID: {product.id}, Name: {product.name}, Category: {product.category.name}")
    print("----------------------------")

    # 4. Передаем в шаблон (для будущего использования)
    context = {
        'latest_products': latest_products,
        'title': 'Главная страница'
    }
    return render(request, 'catalog/home.html', context)

def home(request):
    return render(request, 'catalog/home.html')

def contacts(request):
    if request.method == "POST":
        name = request.POST.get('user_name')
        email = request.POST.get('user_email')
        message = request.POST.get('user_message')
        context = {'success': True, 'name': name}
        return render(request, 'catalog/contacts.html', context)
    return render(request, 'catalog/contacts.html')

def category(request):
    """Контроллер страницы категорий"""
    return render(request, 'catalog/category.html')

def orders(request):
    """Контроллер страницы заказов"""
    return render(request, 'catalog/orders.html')