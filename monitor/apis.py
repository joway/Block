from datetime import datetime

from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from monitor.services import MonitorService
from .models import MonitorTask
from .serializers import MonitorTaskModelSerializer


class MonitorViewSet(viewsets.ModelViewSet):
    queryset = MonitorTask.objects.all()
    serializer_class = MonitorTaskModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.updated_at = datetime.now()
        serializer.save()
        headers = self.get_success_headers(serializer.data)

        return Response(self.get_serializer(instance=serializer.instance).data, status=status.HTTP_201_CREATED,
                        headers=headers)

    @list_route(methods=['POST'])
    def verify(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance = serializer.instance
        ret = {
            'element':  MonitorService.extract_html_block(instance)
        }
        try:
            MonitorService.distribute_task(instance, fake=True)
            instance.delete()
            return Response(data=ret, status=status.HTTP_200_OK)
        except Exception as e:
            ret['exception'] = str(e)
            instance.delete()
            return Response(data=ret, status=status.HTTP_400_BAD_REQUEST)
