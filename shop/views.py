from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.utils.translation import activate
from datetime import date

from .forms import ContactForm, OrderForm, CustomPasswordChangeForm, ProfilePictureForm, CustomUserCreationForm
from .models import Brand, Category, Order, OrderItem, Product, Review, UserProfile


def get_cart(request):
    return request.session.get('cart', {})


def get_favorites(request):
    return request.session.get('favorites', [])


def home(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()
    popular_products = Product.objects.filter(is_popular=True, in_stock=True)[:8]
    if not popular_products:
        popular_products = Product.objects.filter(in_stock=True)[:8]
    reviews = Review.objects.filter(is_active=True, rating__gte=3)
    return render(request, 'shop/home.html', {
        'categories': categories,
        'brands': brands,
        'popular_products': popular_products,
        'reviews': reviews,
    })


def catalog(request):
    products = Product.objects.filter(in_stock=True)
    categories = Category.objects.all()
    brands = Brand.objects.all()

    category_slug = request.GET.get('category')
    brand_slug = request.GET.get('brand')
    search_query = request.GET.get('q', '').strip()

    if category_slug:
        products = products.filter(category__slug=category_slug)
    if brand_slug:
        products = products.filter(brand__slug=brand_slug)
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(brand__name__icontains=search_query)
        )

    return render(request, 'shop/catalog.html', {
        'products': products,
        'categories': categories,
        'brands': brands,
        'current_category': category_slug,
        'current_brand': brand_slug,
        'search_query': search_query,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related = Product.objects.filter(
        category=product.category, in_stock=True
    ).exclude(pk=product.pk)[:4]
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'related_products': related,
    })


def about(request):
    return render(request, 'shop/about.html')


def contacts(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Сообщение отправлено! Мы свяжемся с вами в ближайшее время.')
            return redirect('contacts')
    return render(request, 'shop/contacts.html', {'form': form})


def delivery(request):
    return render(request, 'shop/delivery.html')


def returns(request):
    return render(request, 'shop/returns.html')


def faq(request):
    faq_items = [
        {
            'question': 'Как оформить заказ?',
            'answer': 'Добавьте товары в корзину, перейдите в корзину и заполните форму заказа. Наш менеджер свяжется с вами для подтверждения.',
        },
        {
            'question': 'Как оплатить?',
            'answer': 'Оплата принимается переводом на карту. Реквизиты будут отправлены после подтверждения заказа.',
        },
        {
            'question': 'Доставляете ли вы в мой город?',
            'answer': 'Да, мы доставляем по всему Узбекистану. Стоимость и сроки зависят от вашего города и уточняются при оформлении.',
        },
        {
            'question': 'Можно ли посмотреть товар вживую?',
            'answer': 'Да! У нас есть шоурум в Ташкенте по адресу 2-й пр-д Кипчак 40/12. Время работы: Пн-Сб 11:00-21:00.',
        },
        {
            'question': 'Что делать если товар пришёл с дефектом?',
            'answer': 'Свяжитесь с нами в течение 14 дней. Мы заменим товар или вернём деньги согласно условиям возврата.',
        },
    ]
    return render(request, 'shop/faq.html', {'faq_items': faq_items})


def privacy(request):
    return render(request, 'shop/privacy.html')


def terms(request):
    return render(request, 'shop/terms.html')


def cart_view(request):
    cart = get_cart(request)
    products = []
    total = 0
    for product_id, item in cart.items():
        try:
            product = Product.objects.get(pk=int(product_id))
            quantity = item.get('quantity', 1)
            subtotal = product.price * quantity
            total += subtotal
            products.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            })
        except Product.DoesNotExist:
            continue

    # Pre-fill form with user data if authenticated
    if request.user.is_authenticated:
        initial_data = {
            'name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
        }
        order_form = OrderForm(initial=initial_data)
    else:
        order_form = OrderForm()

    return render(request, 'shop/cart.html', {
        'cart_items': products,
        'total': total,
        'order_form': order_form,
        'user_authenticated': request.user.is_authenticated,
    })


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = get_cart(request)
    key = str(product_id)
    if key in cart:
        cart[key]['quantity'] += 1
    else:
        cart[key] = {'quantity': 1}
    request.session['cart'] = cart
    request.session.modified = True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        count = sum(item['quantity'] for item in cart.values())
        return JsonResponse({'success': True, 'cart_count': count, 'message': f'{product.name} добавлен в корзину'})
    messages.success(request, f'{product.name} добавлен в корзину')
    return redirect(request.META.get('HTTP_REFERER', 'catalog'))


@require_POST
def cart_update(request, product_id):
    cart = get_cart(request)
    key = str(product_id)
    quantity = int(request.POST.get('quantity', 1))
    if quantity <= 0:
        cart.pop(key, None)
    elif key in cart:
        cart[key]['quantity'] = quantity
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')


@require_POST
def cart_remove(request, product_id):
    cart = get_cart(request)
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')


@login_required
@require_POST
def place_order(request):
    cart = get_cart(request)
    if not cart:
        messages.error(request, 'Корзина пуста')
        return redirect('cart')

    form = OrderForm(request.POST)
    if form.is_valid():
        order = form.save(commit=False)
        order.user = request.user
        total = 0
        order.save()
        for product_id, item in cart.items():
            try:
                product = Product.objects.get(pk=int(product_id))
                quantity = item.get('quantity', 1)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_name=product.name,
                    price=product.price,
                    quantity=quantity,
                )
                total += product.price * quantity
            except Product.DoesNotExist:
                continue
        order.total = total
        order.save()
        request.session['cart'] = {}
        request.session.modified = True
        messages.success(request, f'Заказ #{order.pk} успешно оформлен! Мы свяжемся с вами.')
        return redirect('cart')

    products = []
    total = 0
    for product_id, item in cart.items():
        try:
            product = Product.objects.get(pk=int(product_id))
            quantity = item.get('quantity', 1)
            subtotal = product.price * quantity
            total += subtotal
            products.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
        except Product.DoesNotExist:
            continue

    messages.error(request, 'Пожалуйста, заполните все обязательные поля')
    return render(request, 'shop/cart.html', {
        'cart_items': products,
        'total': total,
        'order_form': form,
    })


def favorites_view(request):
    fav_ids = get_favorites(request)
    products = Product.objects.filter(pk__in=fav_ids, in_stock=True)
    return render(request, 'shop/favorites.html', {'products': products})


@require_POST
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # Agar foydalanuvchi kirgan bo'lsa, sessionda saqlaymiz
    favorites = get_favorites(request)
    if product_id in favorites:
        favorites.remove(product_id)
        is_favorited = False
    else:
        favorites.append(product_id)
        is_favorited = True
    request.session['favorites'] = favorites
    request.session.modified = True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'is_favorited': is_favorited, 'favorites_count': len(favorites)})
    return redirect(request.META.get('HTTP_REFERER', 'catalog'))


def account_view(request):
    login_form = AuthenticationForm()
    register_form = CustomUserCreationForm()
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'login':
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.profile.full_name or user.username}!')
                return redirect('account')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль')
                return redirect('account')
        elif action == 'register':
            register_form = CustomUserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                messages.success(request, 'Аккаунт создан!')
                return redirect('account')
            else:
                for field, errors in register_form.errors.items():
                    for error in errors:
                        messages.error(request, error)
        elif action == 'logout':
            logout(request)
            messages.success(request, 'Вы вышли из аккаунта')
            return redirect('account')

    # Get user orders if authenticated
    user_orders = []
    user_favorites = []
    user_profile = None
    password_form = None
    profile_form = None
    
    if request.user.is_authenticated:
        user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
        fav_ids = get_favorites(request)
        user_favorites = Product.objects.filter(pk__in=fav_ids, in_stock=True)
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        password_form = CustomPasswordChangeForm(request.user)
        profile_form = ProfilePictureForm(instance=user_profile)

    return render(request, 'shop/account.html', {
        'login_form': login_form,
        'register_form': register_form,
        'user_orders': user_orders,
        'user_favorites': user_favorites,
        'user_profile': user_profile,
        'password_form': password_form,
        'profile_form': profile_form,
    })


def set_language(request):
    lang = request.POST.get('language', 'ru')
    if lang in ['ru', 'uz']:
        activate(lang)
        request.session['language'] = lang
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
@require_POST
def add_review(request):
    order_id = request.POST.get('order_id')
    author_name = request.POST.get('author_name')
    rating = request.POST.get('rating')
    text = request.POST.get('text')

    order = get_object_or_404(Order, pk=order_id)

    # Check if order belongs to user
    if order.user != request.user:
        messages.error(request, 'Вы можете оставить отзыв только на свой заказ')
        return redirect('account')

    # Check if order is delivered
    if order.status != 'delivered':
        messages.error(request, 'Отзыв можно оставить только после получения заказа')
        return redirect('account')

    # Check if review already exists
    if Review.objects.filter(order_ref=order, user=request.user).exists():
        messages.error(request, 'Вы уже оставили отзыв на этот заказ')
        return redirect('account')

    # Create review
    review = Review.objects.create(
        author_name=author_name,
        author_initial=author_name[:2].upper() if len(author_name) >= 2 else author_name[:1].upper(),
        text=text,
        rating=int(rating),
        review_date=date.today(),
        is_active=True,
        user=request.user,
        order_ref=order
    )

    messages.success(request, 'Спасибо за ваш отзыв!')
    return redirect('account')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            logout(request)
            messages.success(request, 'Пароль успешно изменён! Войдите с новым паролем.')
            return redirect('account')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = CustomPasswordChangeForm(request.user)
    
    return redirect('account')


@login_required
def update_profile_picture(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Фото профиля успешно обновлено!')
        else:
            messages.error(request, 'Ошибка при загрузке фото')
    
    return redirect('account')
