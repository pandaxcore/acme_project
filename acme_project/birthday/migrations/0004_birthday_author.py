# Generated by Django 3.2.16 on 2024-06-04 17:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('birthday', '0003_auto_20240522_0655'),
    ]

    operations = [
        migrations.AddField(
            model_name='birthday',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор записи'),
        ),
    ]
