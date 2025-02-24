from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate



@api_view(['POST'])
def registration_view(request):

    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()

            refresh = RefreshToken.for_user(account)
            token_data ={
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            response_data = serializer.data
            response_data['tokens'] = token_data

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['Post'])
def logout_view(request):
    try:
        refresh_token = request.data.get('refresh')

        if refresh_token:
            RefreshToken(refresh_token).blacklist()
            return Response({"detail": "Successfully logged out."},
                            status=status.HTTP_205_RESET_CONTENT)

        return Response({"detail": "No refresh token provided."},
                        status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
