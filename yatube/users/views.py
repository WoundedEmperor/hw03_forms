from django.views.generic import CreateView

from django.urls import reverse_lazy

from .forms import CreationForm
from .forms import ContactForm
from .models import Contact

from django.shortcuts import render


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


def user_contact(request):
    # Запрашиваем объект модели Contact
    contact = Contact.objects.get(pk=3)

    # Создаём объект формы
    form = ContactForm(instance=contact)

    # И в словаре контекста передаём эту форму в HTML-шаблон
    return render(request, 'users/contact.html', {'form': form})
