"""Docstring."""
from django.db import models

# Импортируем функцию-валидатор.
from .validators import real_age


class Birthday(models.Model):
    """Docstring."""

    first_name = models.CharField("Имя", max_length=20)
    last_name = models.CharField(
        "Фамилия", max_length=20, blank=True, help_text="Необязательное поле"
    )
    birthday = models.DateField('Дата рождения', validators=(real_age,))

    class Meta:
        """Docstring."""

        constraints = (
            models.UniqueConstraint(
                fields=('first_name', 'last_name', 'birthday'),
                name='Unique person constraint',
            ),
        )
