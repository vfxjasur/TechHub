from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('delivery/', views.delivery, name='delivery'),
    path('returns/', views.returns, name='returns'),
    path('faq/', views.faq, name='faq'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/update/<int:product_id>/', views.cart_update, name='cart_update'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/order/', views.place_order, name='place_order'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('favorites/toggle/<int:product_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('account/', views.account_view, name='account'),
    path('account/review/', views.add_review, name='add_review'),
    path('account/change-password/', views.change_password, name='change_password'),
    path('account/update-profile-picture/', views.update_profile_picture, name='update_profile_picture'),
    path('set-language/', views.set_language, name='set_language'),
]
