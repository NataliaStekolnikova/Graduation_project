# views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Users

def register_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email and password:
            user = Users.objects.create_user(email=email, password=password)
            # Default validators: UserAttributeSimilarityValidator, MinimumLengthValidator, CommonPasswordValidator, NumericPasswordValidator
            # Завалидировать емэйл, совпадаел ли эмэйл!!! https://www.abstractapi.com/guides/django-email-validation
            # Закоментировано, пока не сделана форма login
            # return redirect('login')
    return render(request, 'registration.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('desired_page_name')
        else:
            error_message = "Invalid email or password. Please try again."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')
