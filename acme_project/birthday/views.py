"""Docstring."""

# Импортируем класс пагинатора.
# from django.core.paginator import Paginator
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy

from .forms import BirthdayForm
from .models import Birthday
from .utils import calculate_birthday_countdown


# Создаём миксин.
class BirthdayMixin:
    """Docstring."""

    model = Birthday
    success_url = reverse_lazy('birthday:list')


class BirthdayFormMixin:
    """Docstring."""

    form_class = BirthdayForm
    template_name = 'birthday/birthday.html'


class BirthdayUpdateView(BirthdayMixin, UpdateView):
    """Docstring."""

    model = Birthday
    # И здесь все атрибуты наследуются от BirthdayMixin.
    form_class = BirthdayForm


# Добавляем миксин первым по списку родительских классов.
class BirthdayCreateView(BirthdayMixin, CreateView):
    """Docstring."""

    model = Birthday
    # Не нужно описывать атрибуты: все они унаследованы от BirthdayMixin.
    form_class = BirthdayForm


class BirthdayDeleteView(BirthdayMixin, DeleteView):
    """Docstring."""

    model = Birthday
    success_url = reverse_lazy('birthday:list')


# Наследуем класс от встроенного ListView:
class BirthdayListView(ListView):
    """Docstring."""

    # Указываем модель, с которой работает CBV...
    model = Birthday
    # ...сортировку, которая будет применена при выводе списка объектов:
    ordering = 'id'
    # ...и даже настройки пагинации:
    paginate_by = 2


class BirthdayDetailView(DetailView):
    """Docstring."""

    model = Birthday

    def get_context_data(self, **kwargs):
        """Docstring."""
        # Получаем словарь контекста:
        context = super().get_context_data(**kwargs)
        # Добавляем в словарь новый ключ:
        context['birthday_countdown'] = calculate_birthday_countdown(
            # Дату рождения берём из объекта в словаре context:
            self.object.birthday
        )
        # Возвращаем словарь контекста.
        return context


# # Добавим опциональный параметр pk.
# def birthday(request, pk=None):
#     """Docstring."""
#     # Если в запросе указан pk (если получен запрос на редактирование объекта):
#     if pk is not None:
#         # Получаем объект модели или выбрасываем 404 ошибку.
#         instance = get_object_or_404(Birthday, pk=pk)
#     # Если в запросе не указан pk
#     # (если получен запрос к странице создания записи):
#     else:
#         # Связывать форму с объектом не нужно, установим значение None.
#         instance = None
#     # Передаём в форму либо данные из запроса, либо None.
#     # В случае редактирования прикрепляем объект модели.
#     form = BirthdayForm(
#         request.POST or None,
#         # Файлы, переданные в запросе, указываются отдельно.
#         files=request.FILES or None,
#         instance=instance,
#     )
#     # Остальной код без изменений.
#     context = {"form": form}
#     # Сохраняем данные, полученные из формы, и отправляем ответ:
#     if form.is_valid():
#         form.save()
#         birthday_countdown = calculate_birthday_countdown(
#             form.cleaned_data["birthday"]
#             )
#         context.update({"birthday_countdown": birthday_countdown})
#     return render(request, "birthday/birthday.html", context)


# def birthday_list(request):
#     """Docstring."""
#     # Получаем список всех объектов с сортировкой по id.
#     birthdays = Birthday.objects.order_by('id')
#     # Создаём объект пагинатора с количеством 10 записей на страницу.
#     paginator = Paginator(birthdays, 2)

#     # Получаем из запроса значение параметра page.
#     page_number = request.GET.get('page')
#     # Получаем запрошенную страницу пагинатора. 
#     # Если параметра page нет в запросе или его значение не приводится к числу,
#     # вернётся первая страница.
#     page_obj = paginator.get_page(page_number)
#     # Вместо полного списка объектов передаём в контекст 
#     # объект страницы пагинатора
#     context = {'page_obj': page_obj}
#     return render(request, 'birthday/birthday_list.html', context)


# def delete_birthday(request, pk):
#     """Docstring."""
#     # Получаем объект модели или выбрасываем 404 ошибку.
#     instance = get_object_or_404(Birthday, pk=pk)
#     # В форму передаём только объект модели;
#     # передавать в форму параметры запроса не нужно.
#     form = BirthdayForm(instance=instance)
#     context = {"form": form}
#     # Если был получен POST-запрос...
#     if request.method == "POST":
#         # ...удаляем объект:
#         instance.delete()
#         # ...и переадресовываем пользователя на страницу со списком записей.
#         return redirect("birthday:list")
#     # Если был получен GET-запрос — отображаем форму.
#     return render(request, "birthday/birthday.html", context)
