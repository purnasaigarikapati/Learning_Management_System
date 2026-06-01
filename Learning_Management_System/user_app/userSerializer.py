from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def validate_email(self, value):
        data = User.objects.filter(email=value)
        if data.exists():
            raise serializers.ValidationError("email already exists")
        return value

    def validate_username(self, value):
        data = User.objects.filter(name=value)
        if data.exists():
            raise serializers.ValidationError("User already exists")
        return value