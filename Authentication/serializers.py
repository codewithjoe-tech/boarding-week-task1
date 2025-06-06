from rest_framework import serializers
from django.contrib.auth import get_user_model
from .tasks import send_verification_mail

User= get_user_model()



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('email' , 'full_name' , "password" , 'id' ,'is_verified')
        read_only_fields = ( 'id','is_verified')
        

    def create(self, validated_data):
        user = User.objects.create_user(email=validated_data.get('email') , password=validated_data.get('password') , full_name=validated_data.get('full_name'))
        send_verification_mail.delay(validated_data.get('email') , validated_data.get('full_name'))

        return user