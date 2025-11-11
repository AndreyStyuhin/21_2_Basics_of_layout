from django.shortcuts import render

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