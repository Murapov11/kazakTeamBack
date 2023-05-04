import logging

from rest_framework import generics
from api.models import Category, Like, Product
from api.serializers import CategorySerializer2, LikeSerializer2
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.db.models import Subquery, OuterRef
from django.forms.models import model_to_dict


class CategoryListAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer2


class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer2
    lookup_url_kwarg = 'category_id'
    queryset = Category.objects.all()


class LikeAPIView(generics.ListCreateAPIView):  # post and get
    serializer_class = LikeSerializer2
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        likes = Like.objects.filter(user=self.request.user)
        products = Product.objects.filter(id__in=Subquery(likes.values('product')))
        for product in products:
            if Like.objects.filter(product=product).exists():
                product.liked = True
        products_list = [model_to_dict(product) for product in products]
        return JsonResponse(products_list, safe=False)

    def post(self, request, *args, **kwargs):
        try:
            print('nice')
            product = Product.objects.get(pk=request.data.get('product'))
            user = self.request.user
            like = Like.objects.get(product=product, user=user)
            like.delete()
            return JsonResponse({'message': 'Deleted like from database.'})
        except Like.DoesNotExist:
            print('nice')
            product = Product.objects.get(pk=request.data.get('product'))
            user = self.request.user
            Like.objects.create(product=product, user=user)
            return JsonResponse({'message': 'Added like to database.'})

class LikeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LikeSerializer2
    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = 'like_id'

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user)
