from django.shortcuts import render, redirect
from django.views import View
from authentication.forms import RegistrationForm
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from authentication.forms import EditUserProfileForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime




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
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            # Prepare email
            subject = "Welcome to Finance Tracker"
            html_content = render_to_string('email/welcome_email.html', {
                'username': username,
                'year': datetime.now().year
            })
            
            email_msg = EmailMultiAlternatives(
                subject=subject,
                body="You have successfully registered.",
                from_email=None,
                to=[email]
            )
            email_msg.attach_alternative(html_content, "text/html")
            email_msg.send()

            messages.success(request, 'Account created successfully!')
            return redirect('login')
        
        context = {
            'form' : form,
        }
        return render(request, 'authentication/register.html', context)
        

def user_change_pass(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PasswordChangeForm(user = request.user, data = request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Password Changed Successfully')
                return redirect('dashboard')
        else:
            form = PasswordChangeForm(user = request.user)
        context = {
            'form' : form,
        }
        return render(request, 'authentication/changepass.html', context)
    else:
        return redirect('dashboard')


def user_profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = EditUserProfileForm(request.POST, instance = request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile Updated Successfully')
                return redirect('dashboard')
        else:
            form = EditUserProfileForm(instance = request.user)
        context = {
            'form' : form,
        }
        return render(request, 'authentication/user_profile.html', context)
    else:
        return redirect('login')
