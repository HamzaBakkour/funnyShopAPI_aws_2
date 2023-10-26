from rest_framework.serializers import ModelSerializer
from shop.models import Product,\
                            Category
from django.utils.text import slugify
from rest_framework import serializers
from django.db import models



class ProductSerializer(ModelSerializer):


    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["slug"] = Product.objects.get(id=instance.id).slug
        rep["category_name"] = Product.get_category_name(instance)
        rep["category_image"] = self.context['request'].build_absolute_uri(instance.category.image.url)
        rep["category_color"] = Category.get_color_name(instance.category)
        return rep


    def create(self, validated_data):
        try:
            Product.objects.get(name=validated_data['name'])
        except Product.DoesNotExist:
            pass
        else:
            if Product.objects.get(name=validated_data['name']).category == \
                validated_data['category']:
                raise serializers.ValidationError('Product already exists')

        slug = slugify(validated_data['name'])
        validated_data['slug'] = slug
        return Product.objects.create(**validated_data)



    def get_img_url(self, instance):
        self.context['request'].build_absolute_uri(instance.category.image.url)


    def updated(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance


    class Meta:
        model = Product
        fields = [
                    'id',
                    'category',
                    'name',
                    'image',
                    'description',
                    'price',
                    'hb',
                    'attack',
                    'defense',
                    'speed',
                    'available',
                    ]


class CategorySerializer(ModelSerializer):

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["slug"] = Category.objects.get(id=instance.id).slug
        rep["color"] = Category.get_color_name(instance)
        return rep


    def create(self, validated_data):
        try:
            Category.objects.get(name=validated_data['name'])
        except Category.DoesNotExist:
            pass
        else:
            raise serializers.ValidationError('Category already exists')
        
        slug = slugify(validated_data['name'])
        validated_data['slug'] = slug
        return Category.objects.create(**validated_data)


    class Meta:
        model = Category
        fields = ['id',
                    'name',
                    'color',
                    'image',
                    'description']
