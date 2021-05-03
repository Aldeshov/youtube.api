from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response

from additional.models import GameCopyright, SongCopyright, Restrictions
from additional.serializers import GameCopyrightSerializer, SongCopyrightSerializer, RestrictionsSerializer


class GameCopyrightViewSet(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           viewsets.GenericViewSet):

    permission_classes = (IsAdminUser,)
    queryset = GameCopyright.objects.all()
    serializer_class = GameCopyrightSerializer


class SongCopyrightViewSet(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           viewsets.GenericViewSet):
    permission_classes = (IsAdminUser,)
    queryset = SongCopyright.objects.all()
    serializer_class = SongCopyrightSerializer


class GameCopyrightItem(viewsets.ViewSet):

    @staticmethod
    def get_copyright(key):
        try:
            return GameCopyright.objects.get(key=key)
        except GameCopyright.DoesNotExist:
            return None

    @classmethod
    def retrieve(cls, request, key):
        game_copyright = cls.get_copyright(key)
        if game_copyright:
            serializer = GameCopyrightSerializer(game_copyright)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @classmethod
    def update(cls, request, key):
        if not request.user.is_superuser:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        game_copyright = cls.get_copyright(key)
        if game_copyright:
            serializer = GameCopyrightSerializer(instance=game_copyright, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @classmethod
    def destroy(cls, request, key):
        if not request.user.is_superuser:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        game_copyright = cls.get_copyright(key)
        if game_copyright:
            game_copyright.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class SongCopyrightItem(viewsets.ViewSet):

    @staticmethod
    def get_copyright(key):
        try:
            return SongCopyright.objects.get(key=key)
        except SongCopyright.DoesNotExist:
            return None

    @classmethod
    def retrieve(cls, request, key):
        song_copyright = cls.get_copyright(key)
        if song_copyright:
            serializer = SongCopyrightSerializer(song_copyright)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @classmethod
    def update(cls, request, key):
        if not request.user.is_superuser:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        song_copyright = cls.get_copyright(key)
        if song_copyright:
            serializer = SongCopyrightSerializer(instance=song_copyright, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @classmethod
    def destroy(cls, request, key):
        if not request.user.is_superuser:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        song_copyright = cls.get_copyright(key)
        if song_copyright:
            song_copyright.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class RestrictionsViewSet(viewsets.ModelViewSet):
    queryset = Restrictions.objects.all()
    serializer_class = RestrictionsSerializer
    permission_classes = (AllowAny,)
