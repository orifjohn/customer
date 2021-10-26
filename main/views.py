from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Customer
from .forms import CustomerForm, LoginForm, RegisterForm

User = get_user_model()


@login_required(login_url='login-url')
def index_view(request):
    search = request.GET.get('search', None)
    customers = Customer.objects.all()
    if search:
        customers = customers.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(phone_number__icontains=search) |
            Q(address__icontains=search),
        )
    return render(request, 'main/index.html', {'customers': customers})


def customer_add_view(request):
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = Customer(**form.cleaned_data)
            customer.user = request.user
            customer.save()
            return redirect(reverse('index-url'))
    return render(request, 'main/customer_add.html', {'form': form})


def customer_delete_view(request, customer_id):
    if request.method == 'POST':
        customer = get_object_or_404(Customer, id=customer_id)
        customer.delete()
        return redirect(reverse('index-url'))


def customer_edit_view(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            for key, value in request.POST.items():
                setattr(customer, key, value)
                customer.save()
            return redirect(reverse('index-url'))
    return render(request, 'main/customer_edit.html', {'customer': customer, 'form': form})


def register_view(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['password2']:
                user = User.objects.create_user(
                    username=form.cleaned_data.get("username"),
                    password=form.cleaned_data.get("password")
                )
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect(reverse('login-url'))
    return render(request, 'main/register.html', {'form': form})


def login_view(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user:
                login(request, user)
                return redirect(reverse('index-url'))
    return render(request, 'main/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(reverse('index-url'))
