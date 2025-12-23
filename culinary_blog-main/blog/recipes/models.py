from django.db import models
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    """Категория рецепта"""
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(unique=True, verbose_name="URL")
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Рецепт блюда"""
    title = models.CharField(max_length=200, verbose_name="Название рецепта")
    slug = models.SlugField(unique=True, verbose_name="URL")
    description = models.TextField(verbose_name="Описание")
    ingredients = models.TextField(verbose_name="Ингредиенты", help_text="Укажите каждый ингредиент с новой строки")
    instructions = models.TextField(verbose_name="Инструкции по приготовлению")
    cooking_time = models.PositiveIntegerField(verbose_name="Время приготовления (мин)")
    servings = models.PositiveIntegerField(verbose_name="Количество порций", default=1)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")
    image = models.ImageField(upload_to='recipes/', verbose_name="Фотография блюда", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    
    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('recipes:recipe_detail', kwargs={'slug': self.slug})
    
    def get_ingredients_list(self):
        """Возвращает список ингредиентов"""
        return [ing.strip() for ing in self.ingredients.split('\n') if ing.strip()]
