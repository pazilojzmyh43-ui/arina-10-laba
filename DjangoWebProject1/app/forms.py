"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment
from .models import Blog
from .models import Category, CatalogItem

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))


class FeedbackForm(forms.Form):
    #Класс формы отзыва для сайта (лекция 7)
    
    name = forms.CharField(
        label='Ваше имя',
        min_length=2,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иван Иванов'})
    )
    
    email = forms.EmailField(
        label='Ваш e-mail',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    # Как узнали о нас (ChoiceField)
    source = forms.ChoiceField(
        label='Как вы узнали о центре «Пси-Эксперт»?',
        choices=[
            ('', '— выберите —'),
            ('instagram', 'Instagram'),
            ('vk', 'ВКонтакте'),
            ('search', 'Поиск в Яндекс/Google'),
            ('friends', 'От друзей/коллег'),
            ('other', 'Другое'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Оценка сайта (ChoiceField + RadioSelect)
    website_rating = forms.ChoiceField(
        label='Насколько удобен наш сайт?',
        choices=[('5', 'Отлично'), ('4', 'Хорошо'), ('3', 'Средне'), ('2', 'Плохо'), ('1', 'Ужасно')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    
    # Какие аспекты понравились (Multiple checkboxes)
    liked_aspects = forms.MultipleChoiceField(
        label='Что вам особенно понравилось?',
        required=False,
        choices=[
            ('consultation', 'Качество консультации'),
            ('specialist', 'Профессионализм психолога'),
            ('online', 'Удобство онлайн-формата'),
            ('price', 'Цены'),
            ('atmosphere', 'Доверительная атмосфера'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    
    # Рекомендация радиокнопка
    recommend = forms.ChoiceField(
        label='Готовы ли вы рекомендовать центр друзьям?',
        choices=[('yes', 'Да, обязательно'), ('maybe', 'Скорее да'), ('no', 'Пока нет')],
        widget=forms.RadioSelect
    )
    
    # Большой текст textarea
    comments = forms.CharField(
        label='Ваши комментарии и пожелания',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Напишите, что можно улучшить...'})
    )
    
    # Согласие на обработку данных (обязательный флажок)
    consent = forms.BooleanField(
        label='Согласен на обработку персональных данных',
        required=True,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

class RegistrationForm(UserCreationForm):
    """Форма регистрации с Bootstrap-стилями (лекция 8) практика 6"""
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Имя пользователя'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'E-mail'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Пароль'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Подтверждение пароля'
        })

class CommentForm(forms.ModelForm):
    """Форма добавления комментария"""
    
    class Meta:
        model = Comment
        fields = ['text']                    # Только поле с текстом
        labels = {
            'text': 'Комментарий'            # Подпись к полю
        }
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4,
                'placeholder': 'Напишите ваш комментарий...'
            })
        }

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'description', 'image', 'content']   # Поля формы
        labels = {
            'title': 'Заголовок статьи',
            'description': 'Краткое содержание',
            'image': 'Изображение статьи',
            'content': 'Полное содержание статьи'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }


class CategoryForm(forms.ModelForm):
    """Форма добавления категории каталога администратором"""

    class Meta:
        model = Category
        fields = ['name', 'description']
        labels = {
            'name': 'Название категории',
            'description': 'Описание',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class CatalogItemForm(forms.ModelForm):
    """Форма добавления элемента каталога администратором"""

    class Meta:
        model = CatalogItem
        fields = ['name', 'short_description', 'full_description', 'price', 'image', 'category']
        labels = {
            'name': 'Название',
            'short_description': 'Краткое описание',
            'full_description': 'Полное описание',
            'price': 'Цена',
            'image': 'Картинка',
            'category': 'Категория',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'full_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }