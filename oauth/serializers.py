from rest_framework import serializers

from .models import SocialAccount


# Social Auth

class SocialAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccount


class SocialAuthSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=255)

    class Meta:
        model = SocialAccount
        fields = ('provider', 'code')


class SocialProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccount
        fields = ('provider',)


class SocialCallbackSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=255)

    class Meta:
        model = SocialAccount
        fields = ('code',)
