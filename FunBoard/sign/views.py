import random
from string import hexdigits
from django.contrib import messages
from django.core.mail import send_mail
from FunBoard import settings
from .models import OneTimeCode
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            if not user.groups.filter(name='customer').exists():
                login(request, user)
                messages.success(request, ("Верифицируйте аккаунт"))
                return redirect('check_code')
            else:
                login(request, user)
                messages.success(request, ("Вы успешно вошли в систему"))
                return redirect('/')
        else:
            messages.success(request, ("Ошибка авторизации. Попробуйте войти позже."))
            return redirect('login')

    else:
        return render(request, "sign/login.html", {})


def register_view(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            code = ''.join(random.sample(hexdigits, 6))
            send_mail(
                subject='Код активации аккаунта',
                message=f'Ваш код для активации аккаунта: {code}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )
            one_time_code = OneTimeCode(user=user, code=code)
            one_time_code.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Код был отправлен на вашу почту."))
            return redirect('check_code')
        messages.success(request, ("Пароли не совпадают"))
        return redirect('signup')
    return render(request, 'sign/signup.html', {'form': form})


def code_view(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        user = request.user
        if OneTimeCode.objects.filter(user__username=user.username, code=code).exists() and not request.user.groups.filter(name='customer').exists():
            customer_group = Group.objects.get(name='customer')
            customer_group.user_set.add(user)
            OneTimeCode.objects.filter(user=user).delete()
            messages.success(request, ("Аккаунт успешно верифицирован"))
            return redirect('/')
        elif request.user.groups.filter(name='customer').exists():
            messages.success(request, ("Аккаунт уже верифицирован"))
            return redirect('/')
        else:
            return render(request, 'sign/check_code.html', {'message': 'Неверный код'})
    return render(request, 'sign/check_code.html')


def logout_view(request):
        logout(request)
        messages.success(request, ("Вы успешно вышли из системы"))
        return redirect('/')
