from rest_framework import serializers
from django.contrib.auth import get_user_model  # If used custom user model
from accounts.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            name=validated_data["name"],
        )

        return user

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "password",
            "name",
        )
