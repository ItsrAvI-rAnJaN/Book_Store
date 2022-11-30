from rest_framework import serializers
from user.models import User
from .models import Book
from drf_yasg import  openapi


class AllBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'author', 'title', 'price', 'quantity']
        swagger_schema_fields = {"required": ["title", "author","price","quantity","user"], "type": openapi.TYPE_OBJECT}


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'author', 'title', 'price', 'quantity', 'user']
        required_field = ['author', 'title', 'price', 'quantity', "user"]
        user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    def validate(self, attrs):
        user = attrs.get("user")
        if not user.is_superuser:
            raise serializers.ValidationError("UnAuthorized User")
        return super().validate(attrs)
