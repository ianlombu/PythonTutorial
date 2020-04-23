from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import *

from django.forms import inlineformset_factory
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

# hampir sama seperti middleware ========>>> lanjutannya adalah @login_required(login_url='login') ======>> login terlebih dahulu
from django.contrib.auth.decorators import login_required
# ============================================================

# ==========FLASH MESSAGES ==================
from django.contrib import messages


def registerPage(request):
    # form = UserCreationForm()
    # ===============================================
    if request.user.is_authenticated:
        return redirect('home')
    # ===============================================
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                # FLASSH MESSAGES
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def loginPage(request):
    # jika sudah login maka tidak bisa masuk ke logi lagi
    # ===============================================
    if request.user.is_authenticated:
        return redirect('home')
    # ===============================================
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or Password is incorrect')

        context = {}
        return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_order = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'customers': customers,
               'orders': orders, 'total_order': total_order, 'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
def product(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'accounts/products.html', context)


@login_required(login_url='login')
def customer(request, id):
    customers = Customer.objects.get(id=id)
    orders = customers.order_set.all()
    total_order = orders.count()

    # untuk menampilkan form filter
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customers': customers,
               'orders': orders,
               'total_order': total_order,
               'myFilter': myFilter}
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
def createOrder(request, id):
    # extra = 5 =======>>>>>> menampilkan form sebanyak 5
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status',), extra=5)
    customers = Customer.objects.get(id=id)

    # queryset=Order.objects.none() ========>>>>>> untuk menampilkan form kosong
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customers)
    # initial untuk menampilkan data ke form
    # form = OrderForm(initial={'customer': customers})
    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customers)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset': formset}
    return render(request, 'accounts/create_order.html', context)


@login_required(login_url='login')
def updateOrder(request, id):
    order = Order.objects.get(id=id)
    form = OrderForm(instance=order)

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'order': order, 'form': form}
    return render(request, 'accounts/update_order.html', context)


@login_required(login_url='login')
def deleteOrder(request, id):
    order = Order.objects.get(id=id)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'order': order}
    return render(request, 'accounts/delete.html', context)
