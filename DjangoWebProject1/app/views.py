
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from .forms import FeedbackForm

from django.contrib.auth.models import User
from .forms import RegistrationForm

from .models import Blog

from .forms import CommentForm
from .models import Comment

from .forms import BlogForm
from .forms import CategoryForm, CatalogItemForm
from .models import Category, CatalogItem

def home(request):
    # Главная
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    # Контакты
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Страница контактов',
            'year':datetime.now().year,
        }
    )

def about(request):
    # О нас
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def links(request):
    # Ресурсы
    return render(
        request,
        'app/links.html',
        {
            'title': 'Полезные ресурсы',
            'year': datetime.now().year,
        }
    )

def pool(request):
    # Отзывы
    if request.method == 'POST':                    
        form = FeedbackForm(request.POST)           
        if form.is_valid():                         
            data = form.cleaned_data                
            return render(request, 'app/pool.html', {
                'form': None,                       
                'data': data,                       
                'title': 'Спасибо за отзыв',
                'year': datetime.now().year,
            })
    else:
        form = FeedbackForm()                      
    
    return render(request, 'app/pool.html', {
        'form': form,                               
        'title': 'Обратная связь',
        'year': datetime.now().year,
    })

def registration(request):
    """Метод регистрации нового пользователя (лекция 8) практ 6"""
    if request.method == "POST":
        regform = RegistrationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)   # не сохраняем сразу
            reg_f.is_staff = False               # запрещаем вход в админку
            reg_f.is_active = True               # активируем пользователя
            reg_f.is_superuser = False           # не суперпользователь
            reg_f.date_joined = datetime.now()
            reg_f.last_login = datetime.now()
            reg_f.save()
            return redirect('home')              # после регистрации — на главную
    else:
        regform = RegistrationForm()

    return render(
        request,
        'app/registration.html',
        {
            'form': regform,
            'title': 'Регистрация',
            'year': datetime.now().year,
        }
    )

def blog(request):
    """Страница со списком всех статей блога (лента)"""
    posts = Blog.objects.all().order_by('-posted')   # Все статьи, отсортированные по дате (новые сверху)
    
    return render(
        request,
        'app/blog.html',
        {
            'title': 'Блог',
            'posts': posts,                     # Передаём список статей в шаблон
            'year': datetime.now().year,
        }
    )

def blogpost(request, parameter):
    """Страница одной статьи + добавление комментариев"""
    post_1 = Blog.objects.get(id=parameter)     # Получаем статью по id (parameter)
    comments = Comment.objects.filter(post=post_1)   # Все комментарии к этой статье
    
    if request.method == "POST" and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post_1
            comment.author = request.user          # Текущий авторизованный пользователь
            comment.save()
            return redirect('blogpost', parameter=post_1.id)  # Перезагрузка страницы
    else:
        form = CommentForm()
    
    return render(
        request,
        'app/blogpost.html',
        {
            'title': post_1.title,
            'post_1': post_1,                   # Передаём одну статью
            'comments': comments,
            'form': form,
            'year': datetime.now().year,
        }
    )

def newpost(request):
    """Добавление новой статьи блога (только для администратора)"""
    if not request.user.is_superuser:
        return redirect('blog')
    
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)   # request.FILES обязателен для загрузки файлов!
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog')                    # Переадресация на список статей
    else:
        form = BlogForm()
    
    return render(request, 'app/newpost.html', {
        'form': form,
        'title': 'Добавить новую статью',
        'year': datetime.now().year,
    })

def videopost(request):
    """Страница с видео-контентом"""
    return render(request, 'app/videopost.html', {
        'title': 'Видео материалы',
        'year': datetime.now().year,
    })


def catalog(request):
    """Страница «Каталог»: список категорий"""
    categories = Category.objects.all()
    return render(
        request,
        'app/catalog.html',
        {
            'title': 'Каталог',
            'categories': categories,
            'year': datetime.now().year,
        }
    )


def catalog_category(request, parameter):
    """Список элементов выбранной категории. parameter — id категории"""
    category = Category.objects.get(id=parameter)
    items = CatalogItem.objects.filter(category=category)
    return render(
        request,
        'app/catalog_category.html',
        {
            'title': category.name,
            'category': category,
            'items': items,
            'year': datetime.now().year,
        }
    )


def catalog_item(request, parameter):
    """Подробное описание элемента каталога. parameter — id элемента"""
    item = CatalogItem.objects.get(id=parameter)
    return render(
        request,
        'app/catalog_item.html',
        {
            'title': item.name,
            'item': item,
            'year': datetime.now().year,
        }
    )


def newcategory(request):
    """Добавление новой категории каталога (только для администратора)"""
    if not request.user.is_superuser:
        return redirect('catalog')

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('catalog')
    else:
        form = CategoryForm()

    return render(request, 'app/newcategory.html', {
        'form': form,
        'title': 'Добавить категорию',
        'year': datetime.now().year,
    })


def newitem(request):
    """Добавление нового элемента каталога (только для администратора)"""
    if not request.user.is_superuser:
        return redirect('catalog')

    if request.method == "POST":
        form = CatalogItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog')
    else:
        form = CatalogItemForm()

    return render(request, 'app/newitem.html', {
        'form': form,
        'title': 'Добавить услугу',
        'year': datetime.now().year,
    })