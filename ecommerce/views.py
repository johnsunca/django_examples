from django.shortcuts import get_object_or_404, render, redirect
from .forms import EditCartItemForm, CreateOrderForm
from .models import PAYMENT_METHOD_CHOICES, Cart, CartItem, Category, Order, OrderItem, Product
from django.contrib.auth.decorators import (
    user_passes_test,
    permission_required,
    login_required,
)

from faker import Faker
import random, datetime
from django.contrib.auth.models import User


def home(request, category_id=None):
    category = Category.objects.get(id=category_id) if category_id else None
    if category:
        products = Product.objects.filter(category=category).order_by('name')
        context = {
            'category_name': category.name,
            'categories': Category.objects.all(),
            'products': products,
        }
    else:
        products = Product.objects.all()
        context = {
            'categories': Category.objects.all(),
            'products': products,
        }
    return render(request, 'ecommerce/home.html', context)
    
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    products = Product.objects.filter(category=product.category)
    count = products.count()
    similar_products = random.sample(list(products), 4 if count >= 4 else count)
    return render(request, 'ecommerce/product_detail.html', {'product': product, 
                                                             'similar_products': similar_products,
                                                             'categories': Category.objects.all(),})

@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all() # CartItem.objects.filter(cart=cart)
    sub_totals = [item.product.price * item.quantity for item in cart_items]
    total_price = sum(sub_totals)
    forms = [EditCartItemForm(initial={'quantity': cart_items[i].quantity}) for i in range(len(sub_totals))]
    for i in range(len(sub_totals)): 
        forms[i]['quantity'].field.widget.attrs = {'max': cart_items[i].product.quantity, 'min': 1}
    cart_data = [{'cart_item':cart_items[i], 
                  'sub_total':sub_totals[i], 
                  'form': forms[i]} # EditCartItemForm(initial={'quantity': cart_items[i].quantity})} 
                  for i in range(len(sub_totals))]
    return render(request, 'ecommerce/cart_view.html', {'cart': cart, 'cart_data': cart_data,
                                                        'total_price': total_price, 'categories': Category.objects.all(),})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Check if product is available in stock
    if product.quantity > 0:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
        else:
            cart_item.quantity = 1
        cart_item.save()
    return redirect('ecommerce:cart_view')

@login_required
def edit_cart_item(request, cart_item_id):            
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if request.method == 'POST':
        form = EditCartItemForm(request.POST)
        if form.is_valid():
            new_quantity = form.cleaned_data['quantity']
            # Check if the new quantity exceeds the available quantity of the product
            if 1 <= new_quantity <= cart_item.product.quantity:
                old_quantity = cart_item.quantity
                cart_item.quantity = new_quantity
                cart_item.save()                
    return redirect('ecommerce:cart_view')    

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()
    return redirect('ecommerce:cart_view')
    
@login_required
def create_order(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all() 
    if request.method == 'POST':
        form = CreateOrderForm(request.POST)
        if form.is_valid():
            # cart = Cart.objects.get(user=request.user)
            shipping_address = form.cleaned_data['shipping_address']
            payment_method = form.cleaned_data['payment_method']            
            order = Order.objects.create(user=request.user, shipping_address=shipping_address, payment_method=payment_method)            
            # cart_items = cart.items.all()
            for cart_item in cart_items:
                if cart_item.quantity <= cart_item.product.quantity:
                    OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)          
                    # Deduct quantity from available stock
                    cart_item.product.quantity -= cart_item.quantity
                    cart_item.product.save()
            cart.items.clear()
            # add new order id to session
            request.session['last_order'] = order.id
            return redirect('ecommerce:order_detail', order_id=order.id)
    else:
        form = CreateOrderForm()
    sub_totals = [item.product.price * item.quantity for item in cart_items]
    total_price = sum(sub_totals)
    cart_data = [{'cart_item':cart_items[i], 'sub_total':sub_totals[i], } for i in range(len(sub_totals))]
    return render(request, 'ecommerce/create_order.html', 
                  { 'form': form, 'cart_data': cart_data, 
                   'total_price': total_price, 'categories': Category.objects.all(),})

@login_required
def order_list(request):
    if request.user.is_superuser:
        orders = Order.objects.all().order_by('date_ordered')
    else:
        orders = Order.objects.filter(user=request.user).order_by('date_ordered')
    return render(request, 'ecommerce/order_list.html', {'orders': orders, 'categories': Category.objects.all(),})

@login_required
def order_detail(request, order_id=None):
    if not order_id: 
        order_id = request.session['last_order']
    order = Order.objects.get(id=order_id)
    order_items = order.orderitem_set.all()
    sub_totals = [item.product.price * item.quantity for item in order_items]
    total_price = sum(sub_totals)
    order_data = [{'order_item':order_items[i], 'sub_total':sub_totals[i], } for i in range(len(sub_totals))]
    return render(request, 'ecommerce/order_detail.html', { 'order': order,
                  'order_data': order_data, 'total_price': total_price, 'categories': Category.objects.all(),})

@user_passes_test(lambda u: u.is_superuser)
def test_data(request):
    # Delete all objects from all tables
    Category.objects.all().delete()
    Product.objects.all().delete()
    Cart.objects.all().delete()
    CartItem.objects.all().delete()
    Order.objects.all().delete()
    OrderItem.objects.all().delete()

    # Generate test data
    fake = Faker()

    # Create categories
    categories = ['Electronics', 'Clothing', 'Books', 'Home & Kitchen', 'Toys', 
                  'Beauty', 'Sports & Outdoors', 'Automotive', 'Health & Care', ]
    for category_name in categories:
        Category.objects.create(name=category_name)

    # Create products
    for _ in range(200):
        category = random.choice(Category.objects.all())
        product = Product.objects.create(
            name=fake.word(),
            category=category,
            description=fake.text(),
            price=random.uniform(10, 1000),
            quantity=random.randint(1, 100),
        )

    # Create users
    if User.objects.count() < 10:
        for _ in range(10 - User.objects.count()):
            username = fake.user_name()
            email = fake.email()
            password = fake.password()
            User.objects.create_user(username=username, email=email, password=password)

    # Create carts and cart items for each user
    for user in User.objects.all():
        cart = Cart.objects.create(user=user)
        products = random.sample(list(Product.objects.all()), random.randint(1, 10))
        for product in products:
            quantity = random.randint(1, 5)
            CartItem.objects.create(cart=cart, product=product, quantity=quantity)

    # Create orders and order items for users
    users = User.objects.all()
    products = Product.objects.all()
    num_orders = random.randint(1, 100)
    for _ in range(num_orders):
        user = random.choice(list(users))
        shipping_address = fake.address()
        payment_method = random.choice([choice[0] for choice in PAYMENT_METHOD_CHOICES])
        order = Order.objects.create(user=user, shipping_address=shipping_address, payment_method=payment_method)
        
        num_items = random.randint(1, 5)  # Random number of items per order
        selected_products = random.sample(list(products), num_items)
        
        for product in selected_products:
            quantity = random.randint(1, 5)  # Random quantity for each product
            OrderItem.objects.create(order=order, product=product, quantity=quantity)

    return redirect('ecommerce:home')
