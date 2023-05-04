import json

from django.forms import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from api.models import Product, Category, Like

# CRUD - CRATE, READ, UPDATE, DELETE
from api.serializers import CategorySerializer1, CategorySerializer2, ProductSerializer1, ProductSerializer2, ProductSerializer3


@csrf_exempt
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer1(categories, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == 'POST':
        data = json.loads(request.body)
        serializer = CategorySerializer1(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def category_detail(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist as e:
        return JsonResponse({'error': str(e)}, status=400)

    if request.method == 'GET':
        serializer = CategorySerializer2(category)
        return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        data = json.loads(request.body)
        serializer = CategorySerializer2(instance=category, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        category.delete()
        return JsonResponse({'deleted': True})


@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        title = request.GET.get('title')
        if title:
            products = Product.objects.filter(name__icontains=title)
            print(products)
        else:
            products = Product.objects.all()
        for product in products:
            if Like.objects.filter(product=product).exists():
                product.liked = True
        products_list = [model_to_dict(product) for product in products]
        return JsonResponse(products_list, safe=False)
        # serializer = ProductSerializer1(products, many=True)
        # return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        data = json.loads(request.body)
        serializer = ProductSerializer1(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist as e:
        return JsonResponse({'error': str(e)}, status=400)

    if request.method == 'GET':
        serializer = ProductSerializer2(product)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = json.loads(request.body)
        serializer = ProductSerializer3(instance=product, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        product.delete()
        return JsonResponse({'deleted': True})
