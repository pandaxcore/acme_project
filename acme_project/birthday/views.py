"""Docstring."""

# Импортируем класс пагинатора.
# from django.core.paginator import Paginator
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse, reverse_lazy

from .forms import BirthdayForm, CongratulationForm
from .models import Birthday, Congratulation
from .utils import calculate_birthday_countdown
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin


# Создаём миксин.
class BirthdayMixin:
    """Docstring."""

    model = Birthday
    success_url = reverse_lazy('birthday:list')


class BirthdayFormMixin:
    """Docstring."""

    form_class = BirthdayForm
    template_name = 'birthday/birthday.html'


class BirthdayUpdateView(LoginRequiredMixin, BirthdayMixin, UpdateView):
    """Docstring."""

    model = Birthday
    # И здесь все атрибуты наследуются от BirthdayMixin.
    form_class = BirthdayForm


# Добавляем миксин первым по списку родительских классов.
class BirthdayCreateView(LoginRequiredMixin, BirthdayMixin, CreateView):
    """Docstring."""

    model = Birthday
    # Не нужно описывать атрибуты: все они унаследованы от BirthdayMixin.
    form_class = BirthdayForm

    def form_valid(self, form):
        """Docstring."""
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form)


class BirthdayDeleteView(LoginRequiredMixin, BirthdayMixin, DeleteView):
    """Docstring."""

    model = Birthday
    success_url = reverse_lazy('birthday:list')


# Наследуем класс от встроенного ListView:
class BirthdayListView(ListView):
    """Docstring."""

    model = Birthday
    # По умолчанию этот класс
    # выполняет запрос queryset = Birthday.objects.all(),
    # но мы его переопределим:
    queryset = Birthday.objects.prefetch_related('tags')
    ordering = 'id'
    paginate_by = 10


class BirthdayDetailView(DetailView):
    """Docstring."""

    model = Birthday

    def get_context_data(self, **kwargs):
        """Docstring."""
        context = super().get_context_data(**kwargs)
        context['birthday_countdown'] = calculate_birthday_countdown(
            self.object.birthday
        )
        # Записываем в переменную form пустой объект формы.
        context['form'] = CongratulationForm()
        # Запрашиваем все поздравления для выбранного дня рождения.
        context['congratulations'] = (
            # Дополнительно подгружаем авторов комментариев,
            # чтобы избежать множества запросов к БД.
            self.object.congratulations.select_related('author')
        )
        return context


@login_required
def simple_view(request):
    """Docstring."""
    return HttpResponse('Страница для залогиненных пользователей!')


# Будут обработаны POST-запросы только от залогиненных пользователей.
# @login_required
# def add_comment(request, pk):
#     # Получаем объект дня рождения или выбрасываем 404 ошибку.
#     birthday = get_object_or_404(Birthday, pk=pk)
#     # Функция должна обрабатывать только POST-запросы.
#     form = CongratulationForm(request.POST)
#     if form.is_valid():
#         # Создаём объект поздравления, но не сохраняем его в БД.
#         congratulation = form.save(commit=False)
#         # В поле author передаём объект автора поздравления.
#         congratulation.author = request.user
#         # В поле birthday передаём объект дня рождения.
#         congratulation.birthday = birthday
#         # Сохраняем объект в БД.
#         congratulation.save()
#     # Перенаправляем пользователя назад, на страницу дня рождения.
#     return redirect('birthday:detail', pk=pk)

# OR CBV
class CongratulationCreateView(LoginRequiredMixin, CreateView):
    """Docstring."""

    birthday = None
    model = Congratulation
    form_class = CongratulationForm

    # Переопределяем dispatch()
    def dispatch(self, request, *args, **kwargs):
        """Docstring."""
        self.birthday = get_object_or_404(Birthday, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    # Переопределяем form_valid()
    def form_valid(self, form):
        """Docstring."""
        form.instance.author = self.request.user
        form.instance.birthday = self.birthday
        return super().form_valid(form)

    # Переопределяем get_success_url()
    def get_success_url(self):
        """Docstring."""
        return reverse('birthday:detail', kwargs={'pk': self.birthday.pk})


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
