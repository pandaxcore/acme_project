"""Docstring."""
from django.shortcuts import render

from .forms import BirthdayForm
from .models import Birthday


def birthday(request):
    """Docstring."""
    form = BirthdayForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {'form': form}
    return render(request, 'birthday/birthday.html', context)


def birthday_list(request):
    """Docstring."""
    birthdays = Birthday.objects.all()
    context = {'birthdays': birthdays}
    return render(request, 'birthday/birthday_list.html', context)
