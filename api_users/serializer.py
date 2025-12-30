from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','age','music_style','preferred_artists','liked_songs','created_at','updated_at']
        read_only_fields = ['id', 'created_at', 'update_at']

    def validate_age(self, value):
        if value < 0:
            raise serializers.ValidationError("Age must be a positive integer")
        return value
        