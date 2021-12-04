import logging

from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from applications.models import Channel
from applications.serializers import ChannelSerializer
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)


def my_channel(request):
    try:
        return request.user.channel
    except Channel.DoesNotExist:
        return None


class ChannelsViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer

    @classmethod
    def create(cls, request):
        if my_channel(request):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = ChannelSerializer(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            serializer.save()
            logger.info('Channel (' + _(serializer.data.get('name')) + ') has been created')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChannelViewSet(viewsets.GenericViewSet):
    permission_classes = (AllowAny,)

    @classmethod
    def retrieve(cls, request, code):
        filtered_channels = Channel.objects.filter(code=code)
        if not filtered_channels.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        channel = filtered_channels[0]
        serializer = ChannelSerializer(channel, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @classmethod
    def subscribe(cls, request, code):
        filtered_channels = Channel.objects.filter(code=code)
        if not filtered_channels.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        if filtered_channels[0].owner == request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        request.user.profile.subscribe(filtered_channels[0], int(request.query_params.get('undo')) > 0)
        logger.info(f'User {request.user.full_name} subscribed to Channel (' + filtered_channels[0].name + ')')
        return Response(status=status.HTTP_200_OK)

    @classmethod
    def subscribe_status(cls, request, code):
        filtered_channels = Channel.objects.filter(code=code)
        if not filtered_channels.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        if filtered_channels[0].owner == request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        subscribe_status = request.user.profile.is_subscribed(filtered_channels[0])
        return Response({"status": subscribe_status}, status=status.HTTP_200_OK)


class MyChannelViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChannelSerializer

    @classmethod
    def retrieve(cls, request):
        channel = my_channel(request)
        if channel:
            serializer = ChannelSerializer(channel)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def update(cls, request):
        channel = my_channel(request)
        if channel:
            serializer = ChannelSerializer(instance=channel, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info('Channel (' + serializer.data.get('name') + ') has been updated')
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def destroy(cls, request):
        channel = my_channel(request)
        if channel:
            logger.info('Channel (' + channel.name + ') has been deleted')
            channel.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
