from rest_framework import serializers


class DoubanExportSerializer(serializers.Serializer):
    douban_id = serializers.CharField(max_length=255)
