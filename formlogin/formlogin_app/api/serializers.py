from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import serializers
from formlogin_app.models import (CustomUser,  Seller, Investor,
                                  Gamer, Product, OnlineShop, Level, Points)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()


    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid username or password.")


        attrs['user'] = user

        return attrs






class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password','user_type']


###################################################
# Seller and properties serializer


class SellerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Seller
        fields = ['user']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'price', 'description','image']


class OnlineShopSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = OnlineShop
        fields =['name', 'products', 'url', 'description', 'seller']

#################################################
# Gamer serializer


class GamerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Gamer
        fields = ['user']


class LevelSerializer(serializers.ModelSerializer):
    gamer = GamerSerializer()
    class Meta:
        model = Level
        fields = ['gamer', 'level']


class PointsSerializer(serializers.ModelSerializer):
    gamer = GamerSerializer()

    class Meta:
        model = Points
        fields = ['gamer', 'points']


#####################################################
# Investor serializer

class InvestorSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Investor
        fields = ['user', 'investment_amount','portfolio']