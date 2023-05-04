from django.forms import model_to_dict
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse

from api.models import Category,Product, Like
from api.serializers import CategorySerializer2, ProductSerializer1


class CategoryListAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer2(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer2(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailAPIView(APIView):
    def get_object(self, category_id):
        try:
            return Category.objects.get(pk=category_id)
        except Category.DoesNotExist as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, category_id):
        instance = self.get_object(category_id)
        serializer = CategorySerializer2(instance)
        return Response(serializer.data)

    def put(self, request, category_id):
        instance = self.get_object(category_id)
        serializer = CategorySerializer2(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_id):
        instance = self.get_object(category_id)
        instance.delete()
        return Response({'deleted': True})


class CategoryProductListAPIView(APIView):
    def get_object(self, category_id):
        try:
            return Category.objects.get(pk=category_id)
        except Category.DoesNotExist as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, category_id):
        category = self.get_object(category_id)
        user = self.request.user
        products = category.products.all()
        for product in products:
            if Like.objects.filter(product=product).exists():
                product.liked = True
        products_list = [model_to_dict(product) for product in products]
        print(products_list)
        return JsonResponse(products_list, safe=False)
        # serializer = ProductSerializer1(products, many=True)
        # return Response(serializer.data)



