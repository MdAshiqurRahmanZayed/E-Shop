from django.views import generic
from django.core.paginator import Paginator
from product.models import Variant,Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from datetime import datetime
from django.views import View
from product.forms import *
from django.shortcuts import render, redirect


def product_list(request):
    title_query = request.GET.get('title')
    variant_query = request.GET.get('variant')
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    date_query = request.GET.get('date')

    queryset = Product.objects.all()

    if title_query:
        queryset = queryset.filter(title__icontains=title_query)

    if variant_query:
        queryset = queryset.filter(productvariant__variant_title__icontains=variant_query)

    if price_from and price_to:
        queryset = queryset.filter(product_variant__price__range=(price_from, price_to))

    if date_query:
        date = datetime.strptime(date_query, '%Y-%m-%d')
        queryset = queryset.filter(created_at__date=date)

    paginator = Paginator(queryset, 3)  

    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    variants = Variant.objects.all()

    start_index = (products.number - 1) * paginator.per_page + 1
    end_index = min(start_index + paginator.per_page - 1, products.paginator.count)

    return render(request, 'products/list.html', {
        'products': products,
        'variants': variants,
        'start_index': start_index,
        'end_index': end_index,
        'total_count': paginator.count,
    })


class CreateProductView(View):
    template_name = 'products/create.html'

    def get(self, request, *args, **kwargs):
        form = ProductForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect('product:list.product') 
        return render(request, self.template_name, {'form': form})
