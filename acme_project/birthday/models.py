"""Docstring."""
# birthday/models.py
from django.contrib.auth import get_user_model
from django.db import models

# Импортируем функцию-валидатор.
from .validators import real_age

# Импортируем функцию reverse() для получения ссылки на объект.
from django.urls import reverse


# Да, именно так всегда и ссылаемся на модель пользователя!
User = get_user_model()


class Birthday(models.Model):
    """Docstring."""

    first_name = models.CharField("Имя", max_length=20)
    last_name = models.CharField(
        "Фамилия", max_length=20, blank=True, help_text="Необязательное поле"
    )
    birthday = models.DateField('Дата рождения', validators=(real_age,))
    image = models.ImageField('Фото', upload_to='birthdays_images', blank=True)
    author = models.ForeignKey(
        User, verbose_name='Автор записи', on_delete=models.CASCADE, null=True
    )

    class Meta:
        """Docstring."""

        constraints = (
            models.UniqueConstraint(
                fields=('first_name', 'last_name', 'birthday'),
                name='Unique person constraint',
            ),
        )

    def get_absolute_url(self):
        """Docstring."""
        # С помощью функции reverse() возвращаем URL объекта.
        return reverse('birthday:detail', kwargs={'pk': self.pk})


class Congratulation(models.Model):
    text = models.TextField('Текст поздравления')
    birthday = models.ForeignKey(
        Birthday,
        on_delete=models.CASCADE,
        related_name='congratulations'
        )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',)
