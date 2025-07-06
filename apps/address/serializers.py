from .models import Address
from rest_framework import serializers

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

        def validate(self, obj):
            user_id = obj.get('user_id')
            street = obj.get('street_address')
            zip_code = obj.get('zip_code')
            mobile = obj.get('mobile')

            if Address.objects.filter(user_id=user_id, street_address=street, zip_code=zip_code, mobile=mobile).exists():
                raise serializers.ValidationError("This address already exists.")

            return obj