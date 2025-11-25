from django.shortcuts import render, redirect
from .models import Product, Order, OrderItem

# হোমপেজ: প্রোডাক্ট দেখাবে
def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

# কার্টে যোগ করা (সেশন ব্যবহার করে)
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)
    
    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1
    
    request.session['cart'] = cart
    return redirect('index')

# চেকআউট এবং অর্ডার কনফার্ম
def checkout(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    
    cart_items = []
    total = 0
    
    for product in products:
        qty = cart[str(product.id)]
        total += product.price * qty
        cart_items.append({'product': product, 'qty': qty, 'subtotal': product.price * qty})

    if request.method == "POST":
        name = request.POST.get('name')
        address = request.POST.get('address')
        
        # অর্ডার তৈরি
        order = Order.objects.create(customer_name=name, address=address, total_bill=total)
        
        # অর্ডার আইটেম সেভ
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product_name=item['product'].name,
                quantity=item['qty'],
                price=item['product'].price
            )
        
        request.session['cart'] = {} # কার্ট খালি করা
        return render(request, 'success.html')

    return render(request, 'checkout.html', {'cart_items': cart_items, 'total': total})
