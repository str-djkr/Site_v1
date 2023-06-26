
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.catalog, name='catalog'),
    path('cart/', views.cart, name='cart'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('delete-item/<int:product_id>/', views.delete_item, name='delete_item'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('confirm-all-items/', views.confirm_all_items, name='confirm-all-items'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
