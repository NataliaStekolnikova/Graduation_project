from django.shortcuts import render
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