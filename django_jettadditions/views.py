from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import LoginForm, ChangePasswordForm, UserRegistrationForm, UserUpdateForm
from .models import CustomUser
import requests
import phonenumbers

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

def validate_phone(phone):
    try:
        parsed = phonenumbers.parse(phone, None)
        return phonenumbers.is_valid_number(parsed)
    except phonenumbers.NumberParseException:
        return False

def get_data_from_simulator():
    try:
        response = requests.get('http://localhost:5000/get_data', timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

def send_validation_result(data, validation_result):
    try:
        payload = {'data': data, 'result': validation_result}
        response = requests.post('http://localhost:5000/send_result', json=payload, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

def home_view(request):
    return render(request, 'django_jettadditions/home.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = CustomUser.objects.get(username=username)
                if user.is_blocked:
                    return render(request, 'django_jettadditions/login.html', {'form': form, 'error': 'Вы заблокированы. Обратитесь к администратору.'})
                if user.last_login_attempt and (timezone.now() - user.last_login_attempt).days > 30:
                    user.is_blocked = True
                    user.save()
                    return render(request, 'django_jettadditions/login.html', {'form': form, 'error': 'Вы заблокированы. Обратитесь к администратору.'})
                authenticated_user = authenticate(request, username=username, password=password)
                if authenticated_user is not None:
                    user.failed_attempts = 0
                    user.last_login_attempt = timezone.now()
                    user.save()
                    login(request, authenticated_user)
                    if user.role == 'admin' and password == 'initial_password':
                        return redirect('change_password')
                    return render(request, 'django_jettadditions/success.html', {'message': 'Вы успешно авторизовались'})
                else:
                    user.failed_attempts += 1
                    if user.failed_attempts >= 3:
                        user.is_blocked = True
                    user.save()
                    return render(request, 'django_jettadditions/login.html', {'form': form, 'error': 'Неверный логин или пароль'})
            except CustomUser.DoesNotExist:
                return render(request, 'django_jettadditions/login.html', {'form': form, 'error': 'Неверный логин или пароль'})
    else:
        form = LoginForm()
    return render(request, 'django_jettadditions/login.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            if user.check_password(form.cleaned_data['current_password']):
                if form.cleaned_data['new_password'] == form.cleaned_data['confirm_password']:
                    user.set_password(form.cleaned_data['new_password'])
                    user.save()
                    return render(request, 'django_jettadditions/success.html', {'message': 'Пароль успешно изменен'})
                else:
                    return render(request,
                                  'django_jettadditions/change_password.html', {'form': form, 'error': 'Пароли не совпадают'})
            else:
                return render(request, 'django_jettadditions/change_password.html', {'form': form, 'error': 'Неверный текущий пароль'})
    else:
        form = ChangePasswordForm()
    return render(request, 'django_jettadditions/change_password.html', {'form': form})

def validate_view(request):
    result = None
    phone_number = None
    error = None
    if request.method == 'POST':
        if 'get_data' in request.POST:
            data = get_data_from_simulator()
            if data:
                phone_number = data.get('phone')
            else:
                error = 'Не удалось получить данные от симулятора'
        elif 'send_result' in request.POST:
            phone_number = request.POST.get('phone')
            if phone_number:
                is_valid = validate_phone(phone_number)
                result = 'Корректный номер телефона' if is_valid else 'Некорректный номер телефона'
                if not send_validation_result(phone_number, result):
                    error = 'Не удалось отправить результат'
    return render(request, 'django_jettadditions/validate.html', {'phone': phone_number, 'result': result, 'error': error})

@login_required
@user_passes_test(is_admin)
def admin_panel(request):
    users = CustomUser.objects.all()
    return render(request, 'django_jettadditions/admin_panel.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if CustomUser.objects.filter(username=username).exists():
                return render(request, 'django_jettadditions/register_user.html', {'form': form, 'error': 'Пользователь с таким логином уже существует'})
            user = CustomUser.objects.create_user(
                username=username,
                password=form.cleaned_data['password'],
                role=form.cleaned_data['role']
            )
            user.save()
            return redirect('admin_panel')
    else:
        form = UserRegistrationForm()
    return render(request, 'django_jettadditions/register_user.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def update_user(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'django_jettadditions/update_user.html', {'form': form, 'user': user})