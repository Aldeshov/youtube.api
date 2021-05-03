from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from applications.models import Channel
from applications.serializers import ChannelSerializer


class ChannelsViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer

    @classmethod
    def create(cls, request):
        serializer = ChannelSerializer(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChannelViewSet(viewsets.GenericViewSet):
    permission_classes = (AllowAny,)

    @classmethod
    def retrieve(cls, request, code):
        filtered_channels = Channel.objects.filter(code=code)
        if len(filtered_channels) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        channel = filtered_channels[0]
        serializer = ChannelSerializer(channel, many=False)
        return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)


class MyChannelViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChannelSerializer

    @staticmethod
    def my_channel(request):
        try:
            return request.user.channel
        except Channel.DoesNotExist:
            return None

    @classmethod
    def retrieve(cls, request):
        channel = cls.my_channel(request)
        if channel:
            serializer = ChannelSerializer(channel)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def update(cls, request):
        channel = cls.my_channel(request)
        if channel:
            serializer = ChannelSerializer(instance=channel, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def destroy(cls, request):
        channel = cls.my_channel(request)
        if channel:
            channel.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
