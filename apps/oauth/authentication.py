from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.exceptions import InvalidToken, TokenError,AuthenticationFailed


class CustomUserJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):

        header = self.get_header(request)
        if header is None:
            return None
        
        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None
        

        try:
            validated_token = self.get_validated_token(self.get_raw_token(self.get_header(request)))
        except InvalidToken as e:
            raise  AuthenticationFailed("Invalid JWT token")





        app_user_id = validated_token.get("user_id")
        if not app_user_id:
            return None
        try:
            user = User.objects.get(id=app_user_id)
        except User.DoesNotExist:
            return None
        

        request.user = user  # Ensure the correct user is set in request

        


        return (user, validated_token)
    

