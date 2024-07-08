from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.urls import reverse_lazy
from .models import Category, Product, Cart, CartItem
from .forms import UserRegistrationForm, OrderForm
from django.contrib import messages
from django.contrib.auth import login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    categories = Category.objects.all()
    return render(request, 'home.html', {'categories': categories})


@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            cart = Cart.objects.filter(user=request.user).first()
            if cart:
                order = form.save(user=request.user, cart=cart)
                if cart.id:
                    cart.delete()
                    messages.success(request, "Замовлення збережене!")
                else:
                    messages.error(request, "Кошик не може бути видалений, оскільки він не збережений.")
                return redirect('home')
            else:
                messages.error(request, "Кошик не знайдено.")
                return redirect('home')
    else:
        form = OrderForm()

    return render(request, 'create_order.html', {'form': form})


@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        if created:
            cart.save()  # Зберігаємо кошик після його створення
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect('view_cart')
    else:
        product = get_object_or_404(Product, pk=product_id)
        return redirect('category_detail', category_id=product.category_id)

@login_required
def view_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart_items = cart.items.all()
        total = sum(item.product.price * item.quantity for item in cart_items)
    else:
        cart_items = []
        total = 0
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('view_cart')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматичний вхід після реєстрації
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'registration/profile.html')


def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('home'))


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    # Get the sort and search parameters
    sort_by = request.GET.get('sort_by', 'name')
    search_query = request.GET.get('search', '')

    # Filter products by search query
    product_list = Product.objects.filter(category=category, name__icontains=search_query)

    # Sort products
    if sort_by == 'price_asc':
        product_list = product_list.order_by('price')
    elif sort_by == 'price_desc':
        product_list = product_list.order_by('-price')
    else:
        product_list = product_list.order_by('name')

    paginator = Paginator(product_list, 9)  # Пагінація з 9 продуктами на сторінку

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'category_detail.html', {'category': category, 'products': products})


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'product_detail.html', {'product': product})


def contacts(request):
    return render(request, 'contacts.html')
