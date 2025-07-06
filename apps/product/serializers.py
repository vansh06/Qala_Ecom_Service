# serializers.py

from rest_framework import serializers
from .models import Product, Category,Review
from oauth.models import User


class ReviewSerializer(serializers.ModelSerializer):
    # user_id = serializers.IntegerField()  # Use user_id instead of the full user object
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)
    user = serializers.SerializerMethodField()




    class Meta:
        model = Review
        fields = ['id', 'review','rating', 'created_at','user', 'product']
        extra_kwargs = {
            'user_id': {'read_only': True},
            'product': {'read_only': True},
        }

    def get_user(self, obj):
        try:
            user = User.objects.get(id=obj.user_id)
            return {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }
        except User.DoesNotExist:
            return None



class RecursiveCategorySerializer(serializers.Serializer):
    def to_representation(self, value):
        return CategorySerializer(value).data

class CategorySerializer(serializers.ModelSerializer):
    parent = RecursiveCategorySerializer(source='parent_category', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'level', 'parent']

class ProductSerializer(serializers.ModelSerializer):
    
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    category = CategorySerializer()
    reviews = ReviewSerializer(many=True, read_only=True)


    class Meta:
        model = Product
        fields = '__all__'

