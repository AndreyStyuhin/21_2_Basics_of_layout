from catalog.forms import ProductForm
from catalog.models import Product, Category, ContactInfo
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator



def home(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 6)  # 6 товаров на страницу

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'catalog/home.html', {
        'page_obj': page_obj,
        'title': 'Главная страница',
    })



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


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'title': product.name
    })

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'catalog/product_form.html', {'form': form})
