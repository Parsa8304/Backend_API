from rest_framework import status ,  permissions
from rest_framework.response import Response
from .serializers import (CustomUserSerializer, SellerSerializer,ProductSerializer,
                          OnlineShopSerializer,GamerSerializer,LevelSerializer,
                          PointsSerializer ,InvestorSerializer , LoginSerializer, ProductAnalyticsSerializer)

from formlogin_app.models import (CustomUser,  Seller, Investor,
                                  Gamer, Product, OnlineShop, Level, Points)
from rest_framework.permissions import IsAuthenticated ,IsAdminUser , AllowAny
from .permissions import IsSellerOrRead , IsSeller
from rest_framework import viewsets
from ..models import ProductAnalytics
from rest_framework.views import APIView


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
    permission_classes = [IsSeller]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)






class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsSeller]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        analytics_data = self.get_analytics_data(queryset)

        return Response({
            'products': serializer.data,
            'analytics': analytics_data,
        })

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    def get_analytics_data(self, queryset):
        analytics_data = []
        product_ids = queryset.values_list('id', flat=True)
        analytics = ProductAnalytics.objects.filter(product__in=product_ids)


        analytics_dict = {analytics.product.id: analytics for analytics in analytics}

        for product in queryset:
            analytics_item = analytics_dict.get(product.id)
            if analytics_item:
                analytics_data.append({
                    'product_id': product.id,
                    'title': product.title,
                    'views': analytics_item.views,
                    'clicks': analytics_item.clicks,
                    'last_updated': analytics_item.last_updated,
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


        analytics = ProductAnalytics.objects.filter(product=instance).first()
        analytics_data = {
            'product_id': instance.id,
            'title': instance.title,
            'views': analytics.views if analytics else 0,
            'clicks': analytics.clicks if analytics else 0,
            'last_updated': analytics.last_updated if analytics else None,
        }

        return Response({
            'product': serializer.data,
            'analytics': analytics_data,
        })


#####################################################



class TrackClickView(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')
        analytics, created = ProductAnalytics.objects.get_or_create(product_id=product_id)
        analytics.click_count += 1
        analytics.save()
        return Response({'status': 'success', 'click_count': analytics.click_count}, status=status.HTTP_200_OK)

class TrackViewView(APIView):
    def post(self, request):
        product_id = request.data.get('product_id')
        analytics, created = ProductAnalytics.objects.get_or_create(product_id=product_id)
        analytics.view_count += 1
        analytics.save()
        return Response({'status': 'success', 'view_count': analytics.view_count}, status=status.HTTP_200_OK)