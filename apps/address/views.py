from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from oauth.authentication import CustomUserJWTAuthentication
from rest_framework import status

from .models import Address
from .serializers import AddressSerializer

class AddressListCreateView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [CustomUserJWTAuthentication]


    def get(self, request):
        user_id = request.user.id
        print("user id ----->",user_id)
        addresses = Address.objects.filter(user_id=user_id)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()

        required_keys = ['street_address', 'zip_code', 'mobile','state','city']
        missing_keys = [key for key in required_keys if key not in data]

        if missing_keys:
            return Response(
                {'status': '400', 'msg': f'Missing keys: {", ".join(missing_keys)}'},
                status=status.HTTP_400_BAD_REQUEST
            )


        data['user_id'] = request.user.id
        serializer = AddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
