from rest_framework import status ,  permissions
from rest_framework.response import Response
from .serializers import (CustomUserSerializer, SellerSerializer,ProductSerializer,
                          OnlineShopSerializer,GamerSerializer,LevelSerializer,
                          PointsSerializer ,InvestorSerializer , LoginSerializer, ProductAnalyticsSerializer)

from formlogin_app.models import (CustomUser,  Seller, Investor,
                                  Gamer, Product, OnlineShop, Level, Points)
from rest_framework.permissions import IsAuthenticated ,IsAdminUser , AllowAny
from .permissions import IsSellerOrRead
from rest_framework import viewsets
from ..models import ProductAnalytics



class LoginViewSet(viewsets.ViewSet):
    """
    API view for user login.
    """
    serializer_class = LoginSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            context = {
                'message': 'Login successful',
                'username': username,
            }
            return Response(context, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#Seeing all users

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permissions_classes = [IsAdminUser]

#Creating account for any type of user
###############################################

class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


class InvestorViewSet(viewsets.ModelViewSet):
    queryset = Investor.objects.all()
    serializer_class = InvestorSerializer


class GamerViewSet(viewsets.ModelViewSet):
    queryset = Gamer.objects.all()
    serializer_class = GamerSerializer

#adding products
# only if user = seller
###################################3

class OnlineShopViewSet(viewsets.ModelViewSet):
    queryset = OnlineShop.objects.all()
    serializer_class = OnlineShopSerializer
    permissions_classes = [IsSellerOrRead]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsSellerOrRead]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        analytics = ProductAnalytics.objects.all()
        return Response({
            'products': serializer.data,
            'analytics': analytics
        })


    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

# get data for the analytics fo the product ->

    def get_analytics_data(self):
        analytics_data = []
        for product in self.queryset:
            analytics = ProductAnalytics.objects.filter(product=product).first()
            if analytics:
                analytics_data.append({
                    'product_id': product.id,
                    'title': product.title,
                    'views': analytics.views,
                    'clicks': analytics.clicks,
                    'last_updated': analytics.last_updated,
                })
            else:
                analytics_data.append({
                    'product_id': product.id,
                    'title': product.title,
                    'views': 0,
                    'clicks': 0,
                    'last_updated': None,
                })
        return analytics_data

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        analytics_data = self.get_analytics_data()
        return Response({
            'product': serializer.data,
            'analytics': analytics_data
        })

#####################################################