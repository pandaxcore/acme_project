# core/views.py
"""Docstring."""
from django.shortcuts import render


def page_not_found(request, exception):
    """Docstring."""
    # Переменная exception содержит отладочную информацию; 
    # выводить её в шаблон пользовательской страницы 404 мы не станем.
    return render(request, 'acme_project/404.html', status=404)


def csrf_failure(request, reason=''):
    """Docstring."""
    return render(request, 'acme_project/403csrf.html', status=403)
