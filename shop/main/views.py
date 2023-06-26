import uuid

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from pyexpat.errors import messages
from .forms import CartAddProductForm
from .models import Product, CartItem
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, ProductFilterForm
from django.shortcuts import HttpResponse


def index(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('catalog')  # Перенаправлення на головну сторінку після успішного входу
            else:
                invalid_login = True
    else:
        invalid_login = False

    return render(request, 'main\index.html', {'invalid_login': invalid_login})


from .models import Product


def catalog(request):
    products = Product.objects.all()

    # Обробка форми фільтрації
    form = ProductFilterForm(request.GET)
    if form.is_valid():
        name = request.GET.get('name')
        category = form.cleaned_data['category']
        min_price = form.cleaned_data['min_price']
        max_price = form.cleaned_data['max_price']
        # Виконайте фільтрацію товарів на основі переданих параметрів

        # Приклад фільтрації за категорією
        if name:
            products = products.filter(name__icontains=name)

        if category:
            products = products.filter(category=category)

        # Приклад фільтрації за ціною
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)

    context = {'products': products, 'form': form}
    return render(request, 'main/catalog.html', context)



from django.shortcuts import render, redirect
from .models import CartItem


def cart(request):
    if request.method == 'POST':
        variant_id = request.POST.get('variant_id')
        color = request.POST.get('color')
        material = request.POST.get('material')
        cart = request.session.get('cart', {})

        if variant_id in cart:
            cart[variant_id]['color'] = color
            cart[variant_id]['material'] = material
        request.session['cart'] = cart
        request.session.save()

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        color = request.POST.get('color')
        material = request.POST.get('material')

        try:
            item = CartItem.objects.get(product_id=product_id, user=request.user)
            item.quantity = quantity
            item.color = color
            item.material = material
            item.save()
        except CartItem.DoesNotExist:
            pass

        return redirect('cart')  # Перенаправлення на сторінку кошика
    order_id = request.GET.get('order_id')
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    total_price = round(total_price, 2)

    cart_items_with_price = [(item, item.product.price * item.quantity) for item in cart_items]

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_items_with_price': cart_items_with_price,
        'order_id': order_id,  # Додавання 'order_id' у контекст
    }

    return render(request, 'main/cart.html', context)


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    gallery_images = product.gallery_images.all()
    return render(request, 'main/product_detail.html', {'product': product, 'gallery_images': gallery_images})


def delete_item(request, product_id):
    if request.method == 'POST':
        try:
            item = CartItem.objects.get(product_id=product_id, user=request.user)
            item.delete()
            return redirect('cart')
        except CartItem.DoesNotExist:
            return redirect('cart')
    else:
        return redirect('cart')


from django.contrib import messages
from django.core.mail import send_mail

def confirm_all_items(request):
    if request.method == 'POST':
        # Отримати всі елементи кошика
        cart_items = CartItem.objects.filter(user=request.user)

        # Змінити статус кожного елемента на підтверджений
        for item in cart_items:
            item.Success = True
            item.save()

        recipient = 'haliuk.oleh@chnu.edu.ua'  # Адреса отримувача (адміністратора)
        subject = 'Підтвердження замовлення'
        message = 'Ваше замовлення було успішно підтверджено.'

        send_mail(subject, message, 'haliuk.oleh@chnu.edu.ua', [recipient], fail_silently=False)

        messages.success(request, 'Усі товари успішно підтверджено!')

        return redirect('cart')

    return render(request, 'main/cart.html')



def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        cart_product_form = CartAddProductForm(request.POST)
        if cart_product_form.is_valid():
            quantity = cart_product_form.cleaned_data['quantity']
            color = cart_product_form.cleaned_data['color']
            material = cart_product_form.cleaned_data['material']

            # Отримання або створення об'єкта CartItem
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user,  # Поточний користувач
                product=product,
                defaults={
                    'quantity': quantity,
                    'color': color,
                    'material': material,
                }
            )

            # Оновлення значень, якщо об'єкт уже існує
            if not created:
                cart_item.quantity = quantity
                cart_item.color = color
                cart_item.material = material
                cart_item.save()

            # Додати повідомлення до контексту
            message = 'Товар успішно додано в корзину.'
            context = {
                'product': product,
                'cart_product_form': cart_product_form,
                'message': message,
            }

            return render(request, 'main/product_detail.html', context)
    else:
        cart_product_form = CartAddProductForm()

    context = {
        'product': product,
        'cart_product_form': cart_product_form,
    }
    return render(request, 'main/product_detail.html', context)


