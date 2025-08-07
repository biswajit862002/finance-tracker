from django.shortcuts import render, redirect
from django.views import View
from authentication.forms import RegistrationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

class RegisterView(View):
    def get(self, request, *args, **kwergs):
        form = RegistrationForm()
        context = {
            'form' : form,
        }
        return render(request, 'authentication/register.html', context)
    
    def post(self, request, *args, **kwergs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            redirect('/dashboard')


class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwergs):
        return render(request, 'finance/dashboard.html')

