from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm
from .filters import OrderFilter


def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_order = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'customers': customers,
               'orders': orders, 'total_order': total_order, 'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/dashboard.html', context)


def product(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'accounts/products.html', context)


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


def deleteOrder(request, id):
    order = Order.objects.get(id=id)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'order': order}
    return render(request, 'accounts/delete.html', context)
