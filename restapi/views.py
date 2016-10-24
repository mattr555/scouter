from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_extensions.mixins import NestedViewSetMixin
from .models import Team, Note, RobotProperties
from .serializers import UserSerializer, NoteSerializer, TeamSerializer, RobotPropertiesSerializer
from .permissions import IsSelfOrAdminOrReadOnly


@api_view(['GET'])
def me(request):
    return Response(UserSerializer(request.user, context={'request': request}).data)

class UserViewSet(viewsets.ModelViewSet):
    """Get info on all users in the system; or yourself at /me"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsSelfOrAdminOrReadOnly)

    def get_object(self):
        if self.kwargs.get('pk') == "me":
            return self.request.user
        return super(UserViewSet, self).get_object()

    # def list(self, request, *args, **kwargs):
    #     return self.retrieve(request, *args, **kwargs)


class NoteViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()

    def get_queryset(self):
        return super(NoteViewSet, self).get_queryset().filter(owner=self.request.user)

    def perform_create(self, serializer):
        # get team id from url params, so the user only specifies body
        query = self.get_parents_query_dict()
        serializer.save(owner=self.request.user, team_id=query.get('team_id'))


class TeamViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()


    # TODO: investigate ways to do this automatically
    # nested viewset? doesn't seem to work for a single item
    @detail_route(methods=["get", "post"])
    def props(self, request, *args, **kwargs):
        team = self.get_object()
        if request.method == "GET":
            try:
                props = RobotProperties.objects.get(team=team, owner=request.user)
                return Response(RobotPropertiesSerializer(props).data)
            except ObjectDoesNotExist:
                return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        elif request.method == "POST":
            try:
                props = RobotProperties.objects.get(team=team, owner=request.user)
                serializer = RobotPropertiesSerializer(props, data=request.data)
                _status = status.HTTP_200_OK
            except ObjectDoesNotExist:
                serializer = RobotPropertiesSerializer(data=request.data)
                _status = status.HTTP_201_CREATED

            if serializer.is_valid(raise_exception=True):
                serializer.save(team=team, owner=request.user)
                return Response(serializer.data, status=_status)
