from api import views
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
   # path('categories/', views.category_list),
   # path('categories/<int:category_id>/', views.category_detail),
   path('products/', views.product_list),
   path('products/<int:product_id>/', views.product_detail),
   path('categories/', views.CategoryListAPIView.as_view()),
   path('categories/<int:category_id>/', views.CategoryDetailAPIView.as_view()),
   path('categories/<int:category_id>/products/', views.CategoryProductListAPIView.as_view()),
   path('login/', obtain_jwt_token),
   path('registration/', views.registration),
   path('user/', views.get_user),
   path('likes/', views.LikeAPIView.as_view()),
   path('likes/<int:like_id>/', views.LikeDetailAPIView.as_view())
]
