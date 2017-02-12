from rest_framework import serializers

from monitor.models import MonitorTask


class MonitorTaskModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitorTask
        fields = ('name', 'link', 'regex', 'data', 'type', 'frequency')
