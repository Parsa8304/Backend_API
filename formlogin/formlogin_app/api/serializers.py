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

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid username or password.")
            if not user.is_active:
                raise serializers.ValidationError("User account is inactive.")
        else:
            raise serializers.ValidationError("Username and password are required.")

        attrs['user'] = user
        return attrs


###################################################
# Seller and properties serializer
class ProductSerializer(serializers.ModelSerializer):
    onlineshop_name = serializers.CharField(source='online_shop.name', read_only=True)
    class Meta:
        model = Product
        fields = ['title', 'price', 'description','image','online_shop','onlineshop_name']



class SellerSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    online_shop = serializers.SerializerMethodField()

    class Meta:
        model = Seller
        fields = '__all__'

    def get_online_shops(self, obj):
        online_shops = obj.online_shop_set.all()
        return OnlineShopSerializer(online_shops, many=True).data


class OnlineShopSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = OnlineShop
        fields =['name',  'url', 'description', 'seller','products',]

    def to_representation(self, instance):
        return {
            'id': instance.name,
            'name': instance.name,
            'url': instance.url,
            'description': instance.description,
            'seller': instance.seller,
            'products': instance.products,
        }


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