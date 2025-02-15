from rest_framework import status , generics , permissions
from rest_framework.response import Response
from .serializers import (CustomUserSerializer, SellerSerializer,ProductSerializer,
                          OnlineShopSerializer,GamerSerializer,LevelSerializer,
                          PointsSerializer ,InvestorSerializer , LoginSerializer)

from formlogin_app.models import (CustomUser,  Seller, Investor,
                                  Gamer, Product, OnlineShop, Level, Points)
from rest_framework.views import APIView




# User Create view
class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]



class LoginAPIView(APIView):
    """
    API view for user login.
    """
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            user_type = serializer.validated_data['user_type']
            context = {
                'message': 'Login successful',
                'username': username,
                'user_type' : user_type

            }
            return Response(context, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#Seeing all users
class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset , many = True)  # Ensure correct usage
        return Response(serializer.data)


#seeing Only one user
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


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
        serializer = self.get_serializer(queryset, many=True)  # Ensure correct usage
        return Response(serializer.data)


class OnlineShopCreateView(generics.CreateAPIView):
    queryset = OnlineShop.objects.all()
    serializer_class = OnlineShopSerializer



class ProductCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


