from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["email"] = user.email

        return token
    def validate(self, attrs):
        data = super().validate(attrs)

        data["user"] = {
            "id": self.user.id,
            "email": self.user.email,
            "first_name": self.user.first_name,
        }

        return data
    

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()