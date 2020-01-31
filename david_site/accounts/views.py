from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    #redirect to login page, upon successful registration
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
