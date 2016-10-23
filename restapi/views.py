from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_extensions.mixins import NestedViewSetMixin
from .models import Team, Note
from .serializers import UserSerializer, NoteSerializer, TeamSerializer
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
