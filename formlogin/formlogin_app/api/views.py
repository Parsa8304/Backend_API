from rest_framework import status , generics , permissions
from rest_framework.response import Response
from .serializers import (CustomUserSerializer, SellerSerializer,ProductSerializer,
                          OnlineShopSerializer,GamerSerializer,LevelSerializer,
                          PointsSerializer ,InvestorSerializer , LoginSerializer)

from formlogin_app.models import (CustomUser,  Seller, Investor,
                                  Gamer, Product, OnlineShop, Level, Points)
from rest_framework.views import APIView





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
            user = serializer.validated_data['user']
            context = {
                'message': 'Login successful',
                'username': user.username,
                'user_type' : user.user_type

            }
            return Response(context, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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