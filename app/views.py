from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.views.decorators.http import require_POST

from app.forms import UpdateCountForm, OrderForm, AddCommentForm
from app.models import Item, Category, Cart, User, Profile, Order, RatingMark, Comment


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
    comments = Comment.objects.filter(item_id__slug=item_slug)
    form = AddCommentForm()

    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.item = item
            form.save()
            return redirect(item.get_absolute_url())
    context = {
        'item': item,
        'title': title,
        'comments': comments,
        'form': form,
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
    return render(request, 'app/cart.html', {'cart': cart, 'form': form,'title':'Cart'})


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
    user = get_object_or_404(User, id=pk)
    if request.user == user or request.user.is_superuser:
        orders = Order.objects.filter(user_id=pk)
        # items = get_list_or_404(Item,id)
        # items = Item.objects.filter(id__in=product_ids)  # 1 2 3
        # items = get_list_or_404(Item, id__in=)
        context = {
            'user_profile': profile,
            'orders': orders,
            'user': user,
            'title': f"{user.username}'s profile"
        }
        return render(request, 'app/profile.html', context=context)
    else:
        raise Http404("Access forbidden. You can't see another user's profile")


def make_order(request):
    cart = Cart(request)
    is_cart = bool(cart)
    if request.method == 'POST':
        updated_request = request.POST.copy()
        updated_request.update({'total_cost': cart.get_total_price(), 'user': request.user.id})
        form = OrderForm(updated_request)
        order = form.save(commit=False)
        order.user = request.user
        if form.is_valid():
            print(form.cleaned_data)
            print(updated_request)
            order.save()
    else:
        form = OrderForm()
    context = {
        'cart': cart,
        'form': form,
        'title': 'Order',
    }
    return render(request, 'app/order.html', context=context)
