import logging

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User
from authentication.serializers import CreateUserSerializer, BaseUserSerializer, UpdateUserSerializer
from content.serializers import ProfileSerializer

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    @classmethod
    def create(cls, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info('User (' + serializer.data.get('full_name') + ') has been created')
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentUser(APIView):

    @classmethod
    def get(cls, request):
        serializer = BaseUserSerializer(request.user, many=False)
        return Response(serializer.data)

    @classmethod
    def put(cls, request):
        if request.data.get("change_password") is True:
            form = PasswordChangeForm(request.user, request.data)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                logger.info('User (' + request.user.full_name + ') changed password')
                return Response(form.data, status=status.HTTP_200_OK)
            else:
                return Response(form.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = UpdateUserSerializer(instance=request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info('User (' + serializer.data.get('full_name') + ') has been updated')
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @classmethod
    def delete(cls, request):
        logger.info('User (' + request.user.full_name + ') has been deleted')
        request.user.delete()
        return Response(status=status.HTTP_200_OK)


class CurrentUserProfile(APIView):

    @classmethod
    def get(cls, request):
        serializer = ProfileSerializer(request.user.profile)
        return Response(serializer.data)


class ProfileAPIView(APIView):

    @classmethod
    def get(cls, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if user.profile.is_private:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = ProfileSerializer(user.profile)
        return Response(serializer.data)


class UserGenericViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAdminUser,)

    @classmethod
    def retrieve(cls, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BaseUserSerializer(user)
        return Response(serializer.data)
