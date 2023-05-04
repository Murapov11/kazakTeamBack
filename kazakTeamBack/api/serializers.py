from api.models import Category, Product, Like
from rest_framework import serializers


class CategorySerializer1(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()

    def create(self, validated_data):
        category = Category.objects.create(**validated_data)
        return category

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class CategorySerializer2(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class LikeSerializer2(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Like
        fields = ('id', 'product', 'user')


class ProductSerializer1(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(required=False)
    category_id = serializers.IntegerField()
    price = serializers.IntegerField(required=False)
    img = serializers.CharField(required=False)
    liked = serializers.BooleanField(default=True)

    # we know what is the read_only -> it is when we give the answers
    # we know what is the write_only -> it is when (data=request.data) we giving the data

    def create(self, validated_data):
        product_name = validated_data.get('name', '')
        product_description = validated_data.get('description', '')

        # assume that only existing category will be matched
        product_category_id = validated_data.get('category_id')
        product_category = Category.objects.get(id=product_category_id)

        product_price = validated_data.get('price', 0)
        product_image = validated_data.get('img', '')
        product_liked = validated_data.get('liked', False)

        product = Product.objects.create(
            img=product_image,
            description=product_description,
            name=product_name,
            price=product_price,
            liked=product_liked,
            category=product_category
        )
        return product

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)

        # we assume that only existing data will come
        new_category_id = validated_data.get('category_id', instance.category.id)
        instance.category = Category.objects.get(id=new_category_id)

        instance.price = validated_data.get('price', instance.price)
        instance.img = validated_data.get('img', instance.img)
        instance.liked = validated_data.get('liked', instance.liked)
        instance.save()
        return instance


class ProductSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductSerializer3(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(required=False)
    category_id = serializers.IntegerField(required=False)
    price = serializers.IntegerField(required=False)
    img = serializers.CharField(required=False)
    liked = serializers.BooleanField(default=True)

    # we know what is the read_only -> it is when we give the answers
    # we know what is the write_only -> it is when (data=request.data) we giving the data

    def create(self, validated_data):
        product_name = validated_data.get('name', '')
        product_description = validated_data.get('description', '')

        # assume that only existing category will be matched
        product_category_id = validated_data.get('category_id')
        product_category = Category.objects.get(id=product_category_id)

        product_price = validated_data.get('price', 0)
        product_image = validated_data.get('img', '')
        product_liked = validated_data.get('liked', False)

        product = Product.objects.create(
            img=product_image,
            description=product_description,
            name=product_name,
            price=product_price,
            liked=product_liked,
            category=product_category
        )
        return product

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)

        # we assume that only existing data will come
        new_category_id = validated_data.get('category_id', instance.category.id)
        instance.category = Category.objects.get(id=new_category_id)

        instance.price = validated_data.get('price', instance.price)
        instance.img = validated_data.get('img', instance.img)
        instance.liked = validated_data.get('liked', instance.liked)
        instance.save()
        return instance
