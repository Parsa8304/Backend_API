from rest_framework import status , generics , permissions
from rest_framework.response import Response
from .serializers import (CustomUserSerializer, SellerSerializer,ProductSerializer,
                          OnlineShopSerializer,GamerSerializer,LevelSerializer,
                          PointsSerializer ,InvestorSerializer , LoginSerializer)

from formlogin_app.models import (CustomUser,  Seller, Investor,
                                  Gamer, Product, OnlineShop, Level, Points)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated ,IsAdminUser , AllowAny
from .permissions import IsSeller
from rest_framework import viewsets

# Todo : comment the authorization stuff in views
# so we caen test the cod

# User Create view
class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]



class LoginAPIView(APIView):
    """
    API view for user login.
    """
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data,context= {'request' :request})
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
class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset , many = True)
        return Response(serializer.data)


#seeing Only one user
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAdminUser]

#Creating account for any type of user
###############################################

class SellerListCreateView(generics.ListCreateAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


class InvestorListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating investors.
    """
    queryset = Investor.objects.all()
    serializer_class = InvestorSerializer


class GamerListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating gamers.
    """
    queryset = Gamer.objects.all()
    serializer_class = GamerSerializer




#adding products
###################################3

class OnlineShopListView(generics.ListCreateAPIView):
    queryset = OnlineShop.objects.all()
    serializer_class = OnlineShopSerializer

    def get(self, request, *args, **kwargs ):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)  
        return Response(serializer.data)


class OnlineShopCreateView(generics.CreateAPIView):
    queryset = OnlineShop.objects.all()
    serializer_class = OnlineShopSerializer
    permission_classes = [IsSeller]


#
# class ProductCreateView(generics.ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#
# class ProductListView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
# Todo : this view shold be tested tommorow



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
