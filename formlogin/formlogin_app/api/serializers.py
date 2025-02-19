from django.contrib.auth import authenticate
from rest_framework import serializers
from formlogin_app.models import (CustomUser, Seller, Investor, Gamer, Product, OnlineShop, Level, Points)


#LoginSerializer for login action
class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()


    class Meta:
        model = CustomUser
        fields = ['username', 'password']
# error handling for invalid username or password
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


############################################################
#Product and Seller nested serializers
class ProductSerializer(serializers.ModelSerializer):
    onlineshop_name = serializers.CharField(source='online_shop.name', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

class OnlineShopSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)


    class Meta:
        model = OnlineShop
        fields = ['name', 'url', 'description', 'seller', 'products']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['id'] = instance.id
        return representation

class SellerSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    online_shop = serializers.SerializerMethodField()

    class Meta:
        model = Seller
        fields = '__all__'

    def get_online_shop(self, obj):
        online_shops = obj.onlineshop_set.all()
        return OnlineShopSerializer(online_shops, many=True).data

###################################################
#Gamer serializer  and it's properties
class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['level']

class PointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Points
        fields = ['points']

class GamerSerializer(serializers.ModelSerializer):
    level = LevelSerializer(read_only=True)
    points = PointsSerializer(read_only=True)

    class Meta:
        model = Gamer
        fields = ['user', 'level', 'points']

#########################################################
#Investor stuff

class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = ['user', 'portfolio']

######################################################
#Custom user nested serializer

class CustomUserSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)
    gamer = GamerSerializer(many=True, read_only=True)
    investor = InvestorSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = '__all__'


    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
