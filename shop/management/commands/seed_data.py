from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand

from shop.models import Brand, Category, Product, Review


class Command(BaseCommand):
    help = 'Seed TechHub database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        categories_data = [
            {'name': 'Клавиатуры', 'slug': 'keyboards', 'icon': 'keyboard', 'order': 1},
            {'name': 'Мыши', 'slug': 'mice', 'icon': 'mouse', 'order': 2},
            {'name': 'Коврики', 'slug': 'mousepads', 'icon': 'mousepad', 'order': 3},
            {'name': 'Наушники', 'slug': 'headsets', 'icon': 'headphones', 'order': 4},
        ]
        for data in categories_data:
            Category.objects.update_or_create(slug=data['slug'], defaults=data)

        brands_data = [
            'Cyberlynx', 'Zifriend', 'ATK', 'GravaStar', 'Xinmeng', 'Ajazz',
            'Logitech', 'Razer', 'HyperX', 'SteelSeries',
        ]
        for name in brands_data:
            Brand.objects.update_or_create(
                slug=name.lower().replace(' ', '-'),
                defaults={'name': name},
            )

        products_data = [
            {
                'name': 'ATK X1 Pro Wireless',
                'slug': 'atk-x1-pro-wireless',
                'category': 'mice',
                'brand': 'ATK',
                'price': Decimal('890000'),
                'old_price': Decimal('990000'),
                'is_popular': True,
                'image_url': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=400&fit=crop',
                'description': 'Беспроводная игровая мышь с сенсором PAW3395, вес 49г, 8K polling rate.',
            },
            {
                'name': 'Cyberlynx CL-87 Mechanical',
                'slug': 'cyberlynx-cl87',
                'category': 'keyboards',
                'brand': 'Cyberlynx',
                'price': Decimal('1250000'),
                'is_popular': True,
                'image_url': 'https://images.unsplash.com/photo-1587829741301-dc798b03add3?w=400&h=400&fit=crop',
                'description': 'Механическая клавиатура 87 клавиш, переключатели Red, RGB подсветка.',
            },
            {
                'name': 'GravaStar Mercury K1',
                'slug': 'gravastar-mercury-k1',
                'category': 'keyboards',
                'brand': 'GravaStar',
                'price': Decimal('2100000'),
                'is_popular': True,
                'image_url': 'https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?w=400&h=400&fit=crop',
                'description': 'Премиальная механическая клавиатура с уникальным дизайном и Bluetooth.',
            },
            {
                'name': 'Zifriend Z1 Gaming Headset',
                'slug': 'zifriend-z1-headset',
                'category': 'headsets',
                'brand': 'Zifriend',
                'price': Decimal('650000'),
                'is_popular': True,
                'image_url': 'https://images.unsplash.com/photo-1484704849700-f032a568e944?w=400&h=400&fit=crop',
                'description': 'Игровые наушники 7.1 surround, микрофон с шумоподавлением.',
            },
            {
                'name': 'Ajazz AK820 Pro',
                'slug': 'ajazz-ak820-pro',
                'category': 'keyboards',
                'brand': 'Ajazz',
                'price': Decimal('980000'),
                'is_popular': True,
                'image_url': 'https://images.unsplash.com/photo-1541140531918-58539db7b36a?w=400&h=400&fit=crop',
                'description': 'Компактная 75% клавиатура с hot-swap переключателями.',
            },
            {
                'name': 'Xinmeng XM-M800',
                'slug': 'xinmeng-xm-m800',
                'category': 'mice',
                'brand': 'Xinmeng',
                'price': Decimal('450000'),
                'is_popular': True,
                'image_url': 'https://images.unsplash.com/photo-1615663240927-2238b6bbef27?w=400&h=400&fit=crop',
                'description': 'Эргономичная игровая мышь с 6 программируемыми кнопками.',
            },
            {
                'name': 'Cyberlynx Speed Pad XL',
                'slug': 'cyberlynx-speed-pad-xl',
                'category': 'mousepads',
                'brand': 'Cyberlynx',
                'price': Decimal('280000'),
                'is_popular': True,
                'image_url': 'https://images.unsplash.com/photo-1625948515291-69613efd103f?w=400&h=400&fit=crop',
                'description': 'Игровой коврик 900x400мм, поверхность speed type.',
            },
            {
                'name': 'ATK F1 Pro Keyboard',
                'slug': 'atk-f1-pro',
                'category': 'keyboards',
                'brand': 'ATK',
                'price': Decimal('1450000'),
                'is_popular': True,
                'image_url': 'https://images.unsplash.com/photo-1511467592992-8a57bf01d629?w=400&h=400&fit=crop',
                'description': 'Full-size механическая клавиатура с gasket mount конструкцией.',
            },
            {
                'name': 'Logitech G Pro X Superlight 2',
                'slug': 'logitech-gpro-superlight-2',
                'category': 'mice',
                'brand': 'Logitech',
                'price': Decimal('1650000'),
                'image_url': 'https://images.unsplash.com/photo-1615663240927-2238b6bbef27?w=400&h=400&fit=crop',
                'description': 'Легендарная беспроводная мышь для киберспорта, 60г.',
            },
            {
                'name': 'Razer BlackWidow V4',
                'slug': 'razer-blackwidow-v4',
                'category': 'keyboards',
                'brand': 'Razer',
                'price': Decimal('1890000'),
                'image_url': 'https://images.unsplash.com/photo-1595225478664-87596307a212?w=400&h=400&fit=crop',
                'description': 'Механическая клавиатура Razer Green switches, Chroma RGB.',
            },
            {
                'name': 'HyperX Cloud III Wireless',
                'slug': 'hyperx-cloud-iii',
                'category': 'headsets',
                'brand': 'HyperX',
                'price': Decimal('1200000'),
                'image_url': 'https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=400&h=400&fit=crop',
                'description': 'Беспроводные игровые наушники с DTS Headphone:X.',
            },
            {
                'name': 'SteelSeries QcK Heavy XXL',
                'slug': 'steelseries-qck-heavy',
                'category': 'mousepads',
                'brand': 'SteelSeries',
                'price': Decimal('350000'),
                'image_url': 'https://images.unsplash.com/photo-1625948515291-69613efd103f?w=400&h=400&fit=crop',
                'description': 'Профессиональный коврик для мыши, толщина 6мм.',
            },
        ]

        for data in products_data:
            category = Category.objects.get(slug=data.pop('category'))
            brand_name = data.pop('brand')
            brand = Brand.objects.filter(name=brand_name).first()
            Product.objects.update_or_create(
                slug=data['slug'],
                defaults={**data, 'category': category, 'brand': brand},
            )

        reviews_data = [
            {
                'author_name': 'Алексей К.',
                'author_initial': 'А',
                'text': 'Отличный магазин! Заказал мышку ATK, доставили за 2 дня. Качество сборки на высоте, сенсор отличный.',
                'rating': 5,
                'review_date': date(2026, 6, 10),
                'order': 1,
            },
            {
                'author_name': 'Дмитрий М.',
                'author_initial': 'Д',
                'text': 'Брал клавиатуру GravaStar — выглядит потрясающе, печатать одно удовольствие. Рекомендую TechHub!',
                'rating': 5,
                'review_date': date(2026, 5, 22),
                'order': 2,
            },
            {
                'author_name': 'Сарвар У.',
                'author_initial': 'С',
                'text': 'Быстрая доставка в Самарканд, менеджер помог с выбором наушников. Всё оригинальное, с гарантией.',
                'rating': 5,
                'review_date': date(2026, 4, 15),
                'order': 3,
            },
        ]
        for data in reviews_data:
            Review.objects.update_or_create(
                author_name=data['author_name'],
                defaults=data,
            )

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
