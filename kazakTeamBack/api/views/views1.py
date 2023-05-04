import json
from api.models import Category, Product
from django.http.response import JsonResponse
from django.contrib.auth.models import User

# Create your views here.

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@csrf_exempt
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        categories_json = [c.to_json() for c in categories]
        return JsonResponse(categories_json, safe=False)
    if request.method == 'POST':
        data = json.loads(request.body)
        category_name = data.get('name', '')
        category = Category.objects.create(name=category_name)
        return JsonResponse(category.to_json())


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    user = request.user
    data = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
    return JsonResponse(data)


@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    user = User.objects.create_user(username=data.get('username'), password=data.get('password'))
    user.first_name = data.get('first_name')
    user.last_name = data.get('last_name')
    user.save()
    return JsonResponse({"user_name": user.first_name})


@csrf_exempt
def category_detail(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist as e:
        return JsonResponse({'error': str(e)}, status=400)

    if request.method == 'GET':
        return JsonResponse(category.to_json())
    elif request.method == 'PUT':
        data = json.loads(request.body)
        new_category_name = data.get('name', category.name)
        category.name = new_category_name
        category.save()
        return JsonResponse(category.to_json())
    elif request.method == 'DELETE':
        category.delete()
        return JsonResponse({'deleted': True})


@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        products_json = [p.to_json() for p in products]
        return JsonResponse(products_json, safe=False)
    if request.method == 'POST':
        data = json.loads(request.body)
        product_name = data.get('name', '')
        product_description = data.get('description', '')
        # assume that only existing category will be matched
        product_category_id = data.get('category_id')
        product_price = data.get('price', 0)
        product_image = data.get('img', '')
        product_liked = data.get('liked', False)
        product_category = Category.objects.get(id=product_category_id)

        product = Product.objects.create(
            img=product_image,
            description=product_description,
            name=product_name,
            price=product_price,
            liked=product_liked,
            category=product_category
        )
        return JsonResponse(product.to_json())


@csrf_exempt
def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist as e:
        return JsonResponse({'error': str(e)}, status=400)

    if request.method == 'GET':
        return JsonResponse(product.to_json())
    elif request.method == 'PUT':
        data = json.loads(request.body)
        product_name = data.get('name', product.name)
        product_description = data.get('description', product.description)
        product_price = data.get('price', product.price)
        product_image = data.get('img', product.img)
        product_liked = data.get('liked', product.liked)
        product_category_id = data.get('category_id', product.category.id)
        product_category = Category.objects.get(id=product_category_id)
        product.name = product_name
        product.description = product_description
        product.price = product_price
        product.img = product_image
        product.liked = product_liked
        product.category = product_category
        product.save()
        return JsonResponse(product.to_json())
    elif request.method == 'DELETE':
        product.delete()
        return JsonResponse({'deleted': True})
