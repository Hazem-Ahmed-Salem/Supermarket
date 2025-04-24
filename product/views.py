from django.shortcuts import render,redirect
from django.http import Http404
from .models import Product,Stock
# Create your views here.
def add_products(request):
    if request.method == 'POST':
        product = Product.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            price=request.POST.get('price'),
            category=request.POST.get('category'),
            image=request.FILES.get('product_image'),
        )
        stock = Stock.objects.create(
            product=product,
            quantity=request.POST.get('stock'),
            supplier=request.POST.get('supplier'),
        )
        return redirect('product_preview')
    categories = Product.get_category_choices()
    return render(request, 'product/add_products.html',{'categories':categories})

def add_stock(request):
    if request.method == 'POST':
        product = Product.objects.filter(id=request.POST.get('product')).first()
        if not product:
            raise Http404("Product not found")
        if request.method == 'POST':
            stock = Stock.objects.create(
                product=product,
                quantity=request.POST.get('stock'),
                supplier=request.POST.get('supplier'),
            )
            return redirect('product_preview')
    products = Product.objects.all()
    return render(request, 'product/add_stock.html',{'products':products})

def decrease_stock(request):
    if request.method == 'POST':
        product = Product.objects.filter(id=request.POST.get('product')).first()
        if not product:
            raise Http404("Product not found")
        stocks = Stock.objects.filter(product=product)
        decrease_amount = int(request.POST.get('quantity'))
        total_stock = sum(stock.quantity for stock in stocks)
        print(stocks)
        if total_stock < decrease_amount:
            raise Http404("Not enough stock available")
            
        remaining = decrease_amount
        for stock in stocks:
            if remaining <= 0:
                break
            if stock.quantity <= remaining:
                remaining -= stock.quantity
                stock.quantity = 0
                stock.delete()
            else:
                stock.quantity -= remaining
                remaining = 0
                stock.save()
            
        return redirect('product_preview')
    products = Product.objects.all()
    return render(request,'product/decrease_stock.html',{'products':products})

def product_preview(request):
    products = Product.objects.all()
    return render(request, 'product/product_preview.html',{'products':products})

