from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Recipe, Category


def recipe_list(request):
    """Список всех рецептов"""
    recipes = Recipe.objects.filter(is_published=True)
    
    # Фильтрация по категории
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        recipes = recipes.filter(category=category)
    else:
        category = None
    
    # Пагинация
    paginator = Paginator(recipes, 9)  # 9 рецептов на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category,
    }
    return render(request, 'recipes/recipe_list.html', context)


def recipe_detail(request, slug):
    """Детальный просмотр рецепта"""
    recipe = get_object_or_404(Recipe, slug=slug, is_published=True)
    context = {
        'recipe': recipe,
    }
    return render(request, 'recipes/recipe_detail.html', context)
