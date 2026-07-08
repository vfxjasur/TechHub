def cart_context(request):
    cart = request.session.get('cart', {})
    count = sum(item.get('quantity', 0) for item in cart.values())
    return {'cart_count': count}


def favorites_context(request):
    favorites = request.session.get('favorites', [])
    return {'favorites': favorites}


def language_context(request):
    from django.utils.translation import get_language
    lang = get_language()
    
    translations = {
        'ru': {
            'home': 'Главная',
            'catalog': 'Каталог',
            'about': 'О нас',
            'contacts': 'Контакты',
            'search_placeholder': 'Поиск товаров...',
            'search_btn': 'Найти',
            'favorites': 'Избранное',
            'cart': 'Корзина',
            'account': 'Аккаунт',
            'popular_products': 'Популярные товары',
            'see_all': 'Смотреть все',
            'categories': 'Категории',
            'brands': 'Наши бренды',
            'why_choose_us': 'Почему выбирают TechHub',
            'warranty': 'Официальная гарантия',
            'warranty_desc': 'Гарантия от производителя на всю продукцию',
            'fast_delivery': 'Быстрая доставка',
            'fast_delivery_desc': 'Доставка по всему Узбекистану за 1-3 дня',
            'original_products': 'Оригинальная продукция',
            'original_products_desc': 'Только сертифицированные товары',
            'support': 'Поддержка клиентов',
            'support_desc': 'Консультация и помощь 24/7',
            'reviews': 'Отзывы клиентов',
            'footer_desc': 'Премиальный магазин компьютерной периферии',
            'catalog_title': 'Каталог',
            'company': 'Компания',
            'help': 'Помощь',
            'delivery_payment': 'Доставка и оплата',
            'returns': 'Возврат и обмен',
            'privacy': 'Политика конфиденциальности',
            'terms': 'Условия использования',
            'address': 'Учтепа хокимият 15 квартал',
            'phone': '+998 95 182 22 23',
            'email': 'info@techhub.uz',
            'all_rights': 'Все права защищены.',
        },
        'uz': {
            'home': 'Bosh sahifa',
            'catalog': 'Katalog',
            'about': 'Biz haqimizda',
            'contacts': 'Aloqa',
            'search_placeholder': 'Mahsulotlarni qidirish...',
            'search_btn': 'Qidirish',
            'favorites': 'Sevimlilar',
            'cart': 'Savat',
            'account': 'Hisob',
            'popular_products': 'Ommabop mahsulotlar',
            'see_all': 'Barchasini ko\'rish',
            'categories': 'Kategoriyalar',
            'brands': 'Bizning brendlarimiz',
            'why_choose_us': 'Nima uchun TechHubni tanlaymiz',
            'warranty': 'Rasmiy kafolat',
            'warranty_desc': 'Barcha mahsulotlar uchun ishlab chiqaruvchi kafolati',
            'fast_delivery': 'Tez yetkazib berish',
            'fast_delivery_desc': 'O\'zbekiston bo\'ylab 1-3 kun ichida yetkazib berish',
            'original_products': 'Asl mahsulotlar',
            'original_products_desc': 'Faqat sertifikatlangan mahsulotlar',
            'support': 'Mijozlarni qo\'llab-quvvatlash',
            'support_desc': '24/7 maslahat va yordam',
            'reviews': 'Mijozlar sharhlari',
            'footer_desc': 'Kompyuter periferiyasi premium do\'koni',
            'catalog_title': 'Katalog',
            'company': 'Kompaniya',
            'help': 'Yordam',
            'delivery_payment': 'Yetkazib berish va to\'lov',
            'returns': 'Qaytarish va almashtirish',
            'privacy': 'Maxfiylik siyosati',
            'terms': 'Foydalanish shartlari',
            'address': 'Uchtepa hokimyat 15 kvartal',
            'phone': '+998 95 182 22 23',
            'email': 'info@techhub.uz',
            'all_rights': 'Barcha huquqlar himoyalangan.',
        }
    }
    
    return {
        'current_language': lang,
        't': translations.get(lang, translations['ru'])
    }
