from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from app.forms import UpdateCountForm
from app.models import Item, Category, Cart, User, Profile


def main(request):
    items = Item.objects.all()
    categories = Category.objects.all()
    cart = Cart(request)
    cart_len = cart.cart_len()
    context = {
        'items': items,
        'categories': categories,
        'title': 'Main page',
        'category': 'all',
        'cart': cart,
        'cart_len': cart_len,
        'page_name': 'main',
    }
    return render(request, 'app/main.html', context=context)


def show_by_category(request, cat_slug):
    categories = Category.objects.all()
    chosen_category = Category.objects.get(slug=cat_slug)
    items = Item.objects.filter(category=chosen_category)
    title = chosen_category.name
    cart = Cart(request)
    cart_len = cart.cart_len()
    context = {
        'items': items,
        'categories': categories,
        'title': title,
        'cart': cart,
        'cart_len': cart_len,
    }
    return render(request, 'app/main.html', context=context)


def show_item(request, item_slug):
    item = Item.objects.get(slug=item_slug)
    title = item.title
    context = {
        'item': item,
        'title': title,
    }
    return render(request, 'app/item.html', context=context)


@require_POST
def add_to_cart(request, item_slug):
    c = Cart(request)
    item = get_object_or_404(Item, slug=item_slug)
    c.add_product(item)
    return redirect('show_cart')


@require_POST
def remove_from_cart(request, item_slug):
    c = Cart(request)
    item = get_object_or_404(Item, slug=item_slug)
    c.remove(item)
    return redirect('show_cart')


def show_cart(request):
    cart = Cart(request)
    is_cart = bool(cart)
    form = UpdateCountForm
    # item1 = Item.objects.get(id=1)
    # print(cart.session['cart'])
    # cart.change_quantity(item1,5)
    # print(cart.session['cart'])
    return render(request, 'app/cart.html', {'cart': cart, 'form': form})


@require_POST
def update_count(request, item_slug):
    cart = Cart(request)
    form = UpdateCountForm(request.POST)
    print(request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        item = get_object_or_404(Item, slug=item_slug)
        cart.change_quantity(item, form.cleaned_data['quantity'])
    return redirect('show_cart')


def show_profile(request, pk):
    profile = get_object_or_404(Profile, user_id=pk)
    context = {
        'user_profile': profile,
    }
    return render(request, 'app/profile.html', context=context)

def make_order(request):
    pass