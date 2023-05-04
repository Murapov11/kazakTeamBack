from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255)  # by default not null

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def __str__(self):
        return f'{self.id}: {self.name}'


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    # this will writen as category_id in database
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='products')

    price = models.IntegerField()
    img = models.TextField()
    liked = models.BooleanField()

    #   TextField, CharField -> while creating if we not provide  by default it will be empty string

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category_id': self.category.id,
            'price': self.price,
            'img': self.img,
            'liked': self.liked
        }

    def __str__(self):
        return f'{self.id}: {self.name} , {self.description}, {self.category}'


"""
Rules:
1) The Category column of product table can not be null(one product -> one category)
"""


class Like(models.Model):
    product = models.ForeignKey(Product,
                                 on_delete=models.CASCADE,
                                 related_name='likes',
                                )
    user = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                             related_name='likes')

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'



# class Purchase(models.Model):
#     name = models.CharField(max_length=255)  # by default not null
#
#     class Meta:
#         verbose_name = 'Category'
#         verbose_name_plural = 'Categories'
#
#     def to_json(self):
#         return {
#             'id': self.id,
#             'name': self.name
#         }
#
#     def __str__(self):
#         return f'{self.id}: {self.name}'
