from email.headerregistry import Group
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Product, Order
from .forms import ProductForm, OrderForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import auth_users, allowed_users
from django.contrib.auth.models import Group
# Create your views here.


@login_required(login_url='user-login')
def index(request):
    staff_group = Group.objects.get(name='Staff')
    customer = User.objects.filter(groups=staff_group)
    product = Product.objects.all()
    product_count = product.count()
    order = Order.objects.all()
    order_count = order.count()
    customer_count = customer.count()
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.customer = request.user
            obj.save()
            return redirect('dashboard-index')
    else:
        form = OrderForm()
    context = {
        'form': form,
        'order': order,
        'product': product,
        'product_count': product_count,
        'order_count': order_count,
        'customer_count': customer_count,
    }
    return render(request, 'dashboard/index.html', context)

# @login_required 
# def staff(request):
#     workers=User.objects.all()
#     context = {
#         'workers' : workers
#     }
#     return render(request, 'dashboard/staff.html', context)
# @login_required(login_url='user-login')
# def staff(request):
#     # Fetch users who are staff based on some condition, e.g., specific roles or custom logic
#     workers = User.objects.filter(is_staff=True)  # If you're marking staff with `is_staff` field
    
#     staff_count = workers.count()  # Get the count of staff members
    
#     context = {
#         'workers': workers,
#         'staff_count': staff_count  # Pass the staff count to the template
#     }
    
#     return render(request, 'dashboard/staff.html', context)


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['Admin','Staff'])
def products(request):
     # Get the staff group
    staff_group = Group.objects.get(name='Staff')
    
    # Get the customers (users with 'Staff' group)
    customer = User.objects.filter(groups=staff_group)
   
    product = Product.objects.all()
    product_count = product.count()
   
    customer_count = customer.count()
    order = Order.objects.all()
    order_count = order.count()
   
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get('name')
            messages.success(request, f'{product_name} has been added')
            return redirect('dashboard-products')
        else:
            # You can add a message here for form errors
            messages.error(request, 'There was an error adding the product.')
    else:
        form = ProductForm()

    context = {
        'product': product,
        'form': form,
        'customer_count': customer_count,
        'product_count': product_count,
        'order_count': order_count,
    }
    return render(request, 'dashboard/products.html', context)


@login_required(login_url='user-login')
def product_detail(request, pk):
    context = {

    }
    return render(request, 'dashboard/products_detail.html', context)


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['Admin','Staff'])
def customers(request):
    staff_group = Group.objects.get(name='Staff')
    customer = User.objects.filter(groups=staff_group)
    customer_count = customer.count()
    product = Product.objects.all()
    product_count = product.count()
    order = Order.objects.all()
    order_count = order.count()
    context = {
        'customer': customer,
        'customer_count': customer_count,
        'product_count': product_count,
        'order_count': order_count,
    }
    return render(request, 'dashboard/customers.html', context)


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['Admin','Staff'])
def customer_detail(request, pk):
    # customer = User.objects.filter(groups=2)
    staff_group = Group.objects.get(name='Staff')
    customer = User.objects.filter(groups=staff_group)
    customer_count = customer.count()
    product = Product.objects.all()
    product_count = product.count()
    order = Order.objects.all()
    order_count = order.count()
    customers = User.objects.get(id=pk)
    context = {
        'customers': customers,
        'customer_count': customer_count,
        'product_count': product_count,
        'order_count': order_count,

    }
    return render(request, 'dashboard/customers_detail.html', context)


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['Admin','Staff'])
def product_edit(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
    
        form = ProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard-products')
    else:
        form = ProductForm(instance=item)
    context = {
        'form': form,
    }
    return render(request, 'dashboard/products_edit.html', context)


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['Admin','Staff'])
def product_delete(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('dashboard-products')
    context = {
        'item': item
    }
    return render(request, 'dashboard/products_delete.html', context)


@login_required(login_url='user-login')
@allowed_users(allowed_roles=['Admin','Staff'])
def order(request):
      # Get the staff group
    staff_group = Group.objects.get(name='Staff')
    
    # Get the customers (users with 'Staff' group)
    customer = User.objects.filter(groups=staff_group)
    
    order = Order.objects.all()
    order_count = order.count()
    
    customer_count = customer.count()
    product = Product.objects.all()
    product_count = product.count()

    context = {
        'order': order,
        'customer_count': customer_count,
        'product_count': product_count,
        'order_count': order_count,
    }
    return render(request, 'dashboard/order.html', context)

