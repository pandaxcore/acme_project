"""Docstring."""
from django.db import models

# Импортируем функцию-валидатор.
from .validators import real_age

# Импортируем функцию reverse() для получения ссылки на объект.
from django.urls import reverse


class Birthday(models.Model):
    """Docstring."""

    first_name = models.CharField("Имя", max_length=20)
    last_name = models.CharField(
        "Фамилия", max_length=20, blank=True, help_text="Необязательное поле"
    )
    birthday = models.DateField('Дата рождения', validators=(real_age,))
    image = models.ImageField('Фото', upload_to='birthdays_images', blank=True)

    class Meta:
        """Docstring."""

        constraints = (
            models.UniqueConstraint(
                fields=('first_name', 'last_name', 'birthday'),
                name='Unique person constraint',
            ),
        )

    def get_absolute_url(self):
        # С помощью функции reverse() возвращаем URL объекта.
        return reverse('birthday:detail', kwargs={'pk': self.pk})
