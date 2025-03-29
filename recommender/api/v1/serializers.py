from rest_framework import serializers
from recommender.models import User, Product, Rating

class RatingSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    product_name = serializers.CharField(max_length=100)
    score = serializers.FloatField()

class ProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    category = serializers.CharField(max_length=100)

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)