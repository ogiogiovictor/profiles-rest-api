from rest_framework import serializers
from profiles_api.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(max_length=50)
    # email = serializers.emailField(max_length=200, unique=True)
      
    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'name', 'password', 'user_type')
        #exclude = ('password', 'user_permissions', 'groups')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': True,
                'style' : {'input_type': 'password'}
            },   
             'email': {
                'required': True,
                'allow_blank': False
            }
        }
        # fields = "__all__"
        
    
    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user
    
    
    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
 
        return super().update(instance, validated_data)
    
    
    
    # def update(self, instance, validated_data):
    #     """Update user and hash password if it's changed"""
    #     password = validated_data.get('password', None)
    #     if password:
    #         validated_data['password'] = make_password(password)
    #     return super().update(instance, validated_data)
    
    
class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = UserProfile
        fields = ['name', 'email', 'password', 'password2', 'user_type']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'error': 'P1 and P2 should be same!'})

        if UserProfile.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exists!'})

        account = UserProfile(email=self.validated_data['email'], name=self.validated_data['name'])
        account.set_password(password)
        account.save()

        return account
    # def validate(self, data):
    #     """Ensure passwords match"""
    #     if data['password'] != data['password2']:
    #         raise serializers.ValidationError({'error': 'Passwords do not match!'})
    #     return data
    
    
    # def create(self, validated_data):
    #     validated_data.pop('password2')  # Remove password2
    #     user = UserProfile.objects.create_user(**validated_data)
    #     return user