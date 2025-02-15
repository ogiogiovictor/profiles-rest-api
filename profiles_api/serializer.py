from rest_framework import serializers
from profiles_api.models import UserProfile


class HelloSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    
    class Meta:
        model = UserProfile
        exclude = ('password',)
        # fields = "__all__"