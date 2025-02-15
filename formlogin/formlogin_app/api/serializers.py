from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import serializers
from formlogin_app.models import (CustomUser,  Seller, Investor,
                                  Gamer, Product, OnlineShop, Level, Points)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid username or password.")


        attrs['user'] = user

        return attrs



###################################################
# Seller and properties serializer
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'price', 'description','image']


class SellerSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Seller
        fields = '__all__'



class OnlineShopSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = OnlineShop
        fields =['name', 'products', 'url', 'description', 'seller']


#################################################
# Gamer serializer

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['level']


class PointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Points
        fields = [ 'points']

class GamerSerializer(serializers.ModelSerializer):
    level = LevelSerializer(read_only=True)  # Assuming you have a Level model
    points = PointsSerializer(read_only=True)  # Assuming you have a Points model

    class Meta:
        model = Gamer
        fields = ['user', 'level', 'points']  # Include user, level, and points


#####################################################
# Investor serializer

class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = ['user',  'portfolio']  # Include user and investment details



#############################################
class CustomUserSerializer(serializers.ModelSerializer):
    seller = SellerSerializer( read_only=True)
    gamer = GamerSerializer(many=True, read_only=True)
    investor = InvestorSerializer(many=True, read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id','username', 'email', 'password','user_type', 'seller','gamer','investor']