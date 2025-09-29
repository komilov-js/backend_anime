from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import ProfileImg

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2")

    def validate(self, attrs):
        # 1️⃣ Parollar bir xil bo‘lishi kerak
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Parollar mos kelmadi!"})

        # 2️⃣ Username oldindan mavjud bo‘lmasligi kerak
        if User.objects.filter(username=attrs["username"]).exists():
            raise serializers.ValidationError({"username": "Bunday foydalanuvchi nomi allaqachon mavjud!"})

        # 3️⃣ Email oldindan mavjud bo‘lmasligi kerak
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError({"email": "Bu email bilan hisob allaqachon yaratilgan!"})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    profile_img = serializers.ImageField(source="profile_img.image", read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "profile_img")
