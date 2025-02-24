from user_app.models import CustomUser
from rest_framework import serializers




class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={ 'input_type' : 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = [ 'username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def create(self , validated_data):
        password = self.validated_data['password']
        validated_data.pop('password2')

        if 'password2' in validated_data:
            raise serializers.ValidationError('Passwords must match')

        if CustomUser.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError('Email already registered')

        account = CustomUser(**validated_data)
        account.set_password(password)
        account.save()
        return account

