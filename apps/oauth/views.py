from django.shortcuts import render
import logging 
from .authentication import CustomUserJWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenRefreshView
from .serializers import AppUserTokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken,TokenError



logger = logging.getLogger('qalakarwaan')
# Create your views here.
from django.http import HttpResponse



def home(request):
    return HttpResponse("Hello, Django!")


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import RegisterSerializer,LoginSerializer,UserSerializer
from rest_framework.permissions import AllowAny


class RegisterView(APIView):

    permission_classes = [AllowAny]
    authentication_classes = []  # Prevents JWT errors

 
    def post(self, request): 
        data = request.data
        logger.info(f"payload-->{data}")
        print(data)
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []  # Prevents JWT errors # ✅ Ensure no authentication is required
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'status':'200','data':serializer.validated_data, 'msg':'Logged In Sucessfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):

    # authentication_classes = [CustomUserJWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request.user)


        # IMPORTANT: Ensure this is an AppUser instance
        if not isinstance(request.user,User):
            return Response({"detail": "Invalid user."}, status=403)


        serializer = UserSerializer(request.user)
        return Response({'status':'200','msg':serializer.data},status=status.HTTP_200_OK )
    

class AppUserTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = AppUserTokenRefreshSerializer

class AppUserLogoutView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []


    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")

            if not refresh_token:
                return Response({"detail": "Refresh token required."}, status=400)


            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

        except TokenError as e:
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"Something went wrong{e}."}, status=status.HTTP_400_BAD_REQUEST)
