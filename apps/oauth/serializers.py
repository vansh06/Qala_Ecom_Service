from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password,check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from address.models import Address
from address.serializers import AddressSerializer





class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    email = serializers.EmailField()

    class Meta:
        model = User  # ✅ use your custom model
        fields = ["email", "first_name", "last_name", "mobile", "password"]

    def create(self, validated_data):
        # Hash the password manually before saving
        validated_data["password"] = make_password(validated_data["password"])
        return User.objects.create(**validated_data)



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:

            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials, try again.")

        if not check_password(password,user.password):
            print("password not matched")
            raise serializers.ValidationError("Invalid credentials, try again.")
 
        if not user.active:
            raise serializers.ValidationError("User account is disabled.")

        # Generate JWT Tokens
        refresh = RefreshToken()
        refresh['email'] = user.email
        refresh['user_id'] = str(user.id)

        refresh["user_type"] = "app_user"  # optional

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id, 
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        }
    

class UserSerializer(serializers.ModelSerializer):

    address = serializers.SerializerMethodField()



    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'mobile','active','address']

    def get_address(self, obj):
        addresses = Address.objects.filter(user_id=obj.id)
        return AddressSerializer(addresses, many=True).data


class AppUserTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = attrs['refresh']

        try:
            token = RefreshToken(refresh)
            user_id = token['user_id']
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise serializers.ValidationError("App user not found.")

            access_token = str(token.access_token)

            return {
                'access': access_token,
                'refresh': str(token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'active':user.active
                }
            }

        except TokenError as e:
            raise InvalidToken(e.args[0])