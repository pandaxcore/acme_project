"""Docstring."""
from django.shortcuts import render


def homepage(request):
    """Docstring."""
    return render(request, 'pages/index.html')
