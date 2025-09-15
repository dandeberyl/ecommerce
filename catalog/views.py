from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product, Category

# Create your views here.
def home(request):
    latest_products = Product.objects.order_by("-id")[:]
    categories = Category.objects.all()
    return render(request, "catalog/home.html", {
        "latest_products": latest_products,
        "categories": categories,
    })

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    category_id = request.GET.get("category")
    if category_id:
        products = products.filter(category_id=category_id)

    sort = request.GET.get("sort")
    if sort == "price_asc":
        products = products.order_by("price")
    elif sort == "price_desc":
        products = products.order_by("-price")
    elif sort == "newest":
        products = products.order_by("-id")    

    paginator = Paginator(products, 100)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "catalog/product_list.html", {
        "products": page_obj,
        "categories": categories,
    })
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "catalog/product_detail.html", {"product": product})


