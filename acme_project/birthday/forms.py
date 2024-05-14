"""Docstring."""
from django import forms

from .models import Birthday


class BirthdayForm(forms.ModelForm):
    """Docstring."""

    class Meta:
        """Docstring."""

        model = Birthday
        fields = '__all__'
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'})
        }
