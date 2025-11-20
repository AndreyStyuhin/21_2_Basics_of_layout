from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from catalog.forms import ProductForm
from catalog.models import Product, Category, ContactInfo
from blog.models import Blog


class ProductListView(ListView):
    """
    Главная страница. Выводит список товаров с пагинацией.
    """
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'page_obj'  # Чтобы не менять цикл в шаблоне home.html
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        # Добавляем 3 последние опубликованные статьи
        context['latest_articles'] = Blog.objects.filter(is_published=True).order_by('-created_at')[:3]

        return context


class ContactView(TemplateView):
    """
    Страница контактов. Обрабатывает GET (отображение) и POST (обратная связь).
    """
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем контактные данные (первую запись)
        context['contact_data'] = ContactInfo.objects.first()
        context['title'] = 'Контакты'
        return context

    def post(self, request, *args, **kwargs):
        # Получаем данные из POST-запроса
        name = request.POST.get('user_name')
        email = request.POST.get('user_email')
        message = request.POST.get('user_message')

        # Логика вывода в консоль (как было в FBV)
        print(f"--- Сообщение с контактов ---")
        print(f"Имя: {name}, Email: {email}")
        print(f"Сообщение: {message}")
        print("----------------------------")

        # Формируем контекст для ответа (остаемся на той же странице)
        context = self.get_context_data(**kwargs)
        context.update({
            'success': True,
            'name': name,
        })
        return self.render_to_response(context)


class CategoryListView(ListView):
    """
    Страница категорий.
    """
    model = Category
    template_name = 'catalog/category.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Проверяем GET-параметр category для фильтрации товаров (логика из шаблона)
        category_pk = self.request.GET.get('category')
        if category_pk:
            context['products'] = Product.objects.filter(category_id=category_pk)
        return context


class OrdersView(TemplateView):
    """Страница заказов (пока просто шаблон)"""
    template_name = 'catalog/orders.html'


class ProductDetailView(DetailView):
    """
    Детальный просмотр товара.
    """
    model = Product
    template_name = 'catalog/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context


class ProductCreateView(CreateView):
    """
    Создание нового товара.
    """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    # Используем reverse_lazy для перенаправления, так как URL еще не загружены при инициализации класса
    success_url = reverse_lazy('home')