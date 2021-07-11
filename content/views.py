import logging

from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework.response import Response
from rest_framework import viewsets, status

from applications.models import Channel
from content.models import Comment, VideoContent, Playlist, Status
from content.serializers import CommentSerializer, VideoContentSerializer, PlaylistSerializer, StatusSerializer

logger = logging.getLogger(__name__)


@api_view(['GET', 'POST'])
def comments(request, code):
    if request.method == 'GET':
        objects = Comment.objects.filter(content__code=code)
        serializer = CommentSerializer(objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        content = VideoContent.objects.filter(code=code)
        if not content.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data, context={
            "channel": request.user.channel,
            "content": content[0]
        })
        if serializer.is_valid():
            serializer.save()
            logger.info('User Channel (' + request.user.channel.__str__() +
                        ') commented Content (' + content[0].__str__() + ')')
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST'])
def my_comments(request, code):
    if request.method == 'GET':
        objects = Comment.objects.filter(content__code=code, owner=request.user.channel)
        serializer = CommentSerializer(objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
def my_comment(request, code, comment_id):
    if request.method == 'GET':
        comment = Comment.objects.filter(id=comment_id, content__code=code, owner=request.user.channel)
        if comment.exists():
            serializer = CommentSerializer(comment[0])
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'PUT':
        comment = Comment.objects.filter(id=comment_id, content__code=code, owner=request.user.channel)
        if comment.exists():
            serializer = CommentSerializer(instance=comment[0], data={
                "text": request.data.get("text"),
                "content": code
            })
            if serializer.is_valid():
                serializer.save()
                logger.info('User Channel (' + request.user.channel.__str__() +
                            ') updated comment on Content (# ' + code + ')')
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'DELETE':
        comment = Comment.objects.filter(id=comment_id, content__code=code, owner=request.user.channel)
        if comment.exists():
            logger.info('User Channel (' + request.user.channel.__str__() +
                        ') deleted comment on Content (# ' + code + ')')
            comment[0].delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class VideoContentsViewSet(viewsets.ModelViewSet):
    queryset = VideoContent.objects.all()
    serializer_class = VideoContentSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    @classmethod
    def list(cls, request):
        contents = VideoContent.objects.all()
        serializer = VideoContentSerializer(contents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @classmethod
    def create(cls, request):
        serializer = VideoContentSerializer(data=request.data, context={
            "channel": request.user.channel
        })
        if serializer.is_valid():
            serializer.save()
            logger.info('User Channel (' + request.user.channel.__str__() +
                        ') created Content (' + serializer.data.get('title') + ')')
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VideoContentViewSet(viewsets.ViewSet):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    @classmethod
    def retrieve(cls, request, code):
        content = VideoContent.objects.filter(code=code)
        if not content.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            content[0].view_content(request.user.channel)
        except Channel.DoesNotExist:
            pass

        serializer = VideoContentSerializer(content[0])
        return Response(serializer.data, status=status.HTTP_200_OK)

    @classmethod
    def like(cls, request, code):
        content = VideoContent.objects.filter(code=code)
        if not content.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            content[0].like_content(request.user.channel,
                                    int(request.query_params.get('dislike')) > 0,
                                    int(request.query_params.get('retract')) > 0)
            logger.info('User Channel (' + request.user.channel.__str__() +
                        ') liked the Content (' + content[0].__str__() + ')')
        except Channel.DoesNotExist:
            Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

    @classmethod
    def save(cls, request, code):
        content = VideoContent.objects.filter(code=code)
        if not content.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        request.user.profile.save_content(content[0], int(request.query_params.get('undo')) > 0)
        logger.info('User Channel (' + request.user.channel.__str__() +
                    ') saved the Content (' + content[0].__str__() + ')')
        return Response(status=status.HTTP_200_OK)


class MyVideoContentsViewSet(viewsets.ViewSet):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    @classmethod
    def list(cls, request):
        contents = VideoContent.objects.filter(on_channel=request.user.channel)
        serializer = VideoContentSerializer(contents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyVideoContentViewSet(viewsets.ViewSet):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    @classmethod
    def retrieve(cls, request, code):
        content = VideoContent.objects.filter(code=code, on_channel=request.user.channel)
        if not content.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = VideoContentSerializer(content[0])
        return Response(serializer.data, status=status.HTTP_200_OK)

    @classmethod
    def update(cls, request, code):
        content = VideoContent.objects.filter(code=code, on_channel=request.user.channel)
        if not content.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = VideoContentSerializer(instance=content[0], data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info('User Channel (' + request.user.channel.__str__() +
                        ') updated the Content (' + content[0].__str__() + ')')
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @classmethod
    def destroy(cls, request, code):
        content = VideoContent.objects.filter(code=code, on_channel=request.user.channel)
        if not content.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        logger.info('User Channel (' + request.user.channel.__str__() +
                    ') deleted the Content (' + content[0].__str__() + ')')
        content[0].delete()
        return Response(status=status.HTTP_200_OK)


class PlaylistViewSet(viewsets.ViewSet):
    @classmethod
    def create(cls, request):
        serializer = PlaylistSerializer(data=request.data, context={
            "channel": request.user.channel
        })
        if serializer.is_valid():
            serializer.save()
            logger.info('User Channel (' + request.user.channel.__str__() +
                        ') created the Playlist (' + serializer.data.get('title') + ')')
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @classmethod
    def retrieve(cls, request, key):
        playlist = Playlist.objects.filter(key=key)
        if not playlist.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PlaylistSerializer(playlist[0])
        return Response(serializer.data, status=status.HTTP_200_OK)

    @classmethod
    def save(cls, request, key):
        playlist = Playlist.objects.filter(key=key)
        if not playlist.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        request.user.profile.save_playlist(playlist[0], int(request.query_params.get('undo')) > 0)
        logger.info('User Channel (' + request.user.channel.__str__() +
                    ') saved the Playlist (' + playlist[0].__str__() + ')')
        return Response(status=status.HTTP_200_OK)


class MyPlaylistsViewSet(viewsets.ViewSet):
    @classmethod
    def list(cls, request):
        playlist = Playlist.objects.filter(owner=request.user.channel)
        serializer = PlaylistSerializer(playlist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @classmethod
    def retrieve(cls, request, key):
        playlist = Playlist.objects.filter(key=key, owner=request.user.channel)
        if not playlist.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PlaylistSerializer(playlist[0])
        return Response(serializer.data, status=status.HTTP_200_OK)

    @classmethod
    def update(cls, request, key):
        playlist = Playlist.objects.filter(key=key, owner=request.user.channel)
        if not playlist.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PlaylistSerializer(instance=playlist[0], data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info('User Channel (' + request.user.channel.__str__() +
                        ') updated the Playlist (' + playlist[0].__str__() + ')')
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @classmethod
    def destroy(cls, request, key):
        playlist = Playlist.objects.filter(key=key, owner=request.user.channel)
        if not playlist.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        logger.info('User Channel (' + request.user.channel.__str__() +
                    ') deleted the Playlist (' + playlist[0].__str__() + ')')
        playlist[0].delete()
        return Response(status=status.HTTP_200_OK)


class StatusViewSet(viewsets.ViewSet):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    @classmethod
    def retrieve(cls, request, code):
        channel = Channel.objects.filter(code=code)
        if not channel.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            serializer = StatusSerializer(channel[0].status)
        except Status.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyStatusViewSet(viewsets.ViewSet):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    @classmethod
    def create(cls, request):
        try:
            channel = request.user.channel
        except Channel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            check = channel.status
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Status.DoesNotExist:
            pass

        serializer = StatusSerializer(data=request.data, context={
            'channel': channel
        })
        if serializer.is_valid():
            serializer.save()
            logger.info('User Channel (' + request.user.channel.__str__() +
                        ') created Status (' + serializer.data.get('title') + ')')
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @classmethod
    def retrieve(cls, request):
        try:
            channel = request.user.channel
            content = channel.status
        except (Channel.DoesNotExist, Status.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = StatusSerializer(content)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @classmethod
    def update(cls, request):
        try:
            channel = request.user.channel
            content = channel.status
        except (Channel.DoesNotExist, Status.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = StatusSerializer(instance=content, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info('User Channel (' + request.user.channel.__str__() +
                        ') updated the Status (' + channel.status.__str__() + ')')
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @classmethod
    def destroy(cls, request):
        try:
            channel = request.user.channel
            content = channel.status
        except (Channel.DoesNotExist, Status.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

        logger.info('User Channel (' + request.user.channel.__str__() +
                    ') deleted the Status (' + channel.status.__str__() + ')')
        content.delete()
        return Response(status=status.HTTP_200_OK)
