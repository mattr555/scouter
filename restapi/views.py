from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Team, Note
from .serializers import UserSerializer, NoteSerializer, TeamSerializer


@api_view(['GET'])
def me(request):
    return Response(UserSerializer(request.user, context={'request': request}).data)

class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Get info on all users in the system; or yourself at /me"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        if self.kwargs.get('pk') == "me":
            return self.request.user
        return super(UserViewSet, self).get_object()

    # def list(self, request, *args, **kwargs):
    #     return self.retrieve(request, *args, **kwargs)


class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer

    def get_queryset(self):
        return self.request.user.notes.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()

    # @detail_route(permission_classes=[permissions.IsAuthenticated])
    # def get_notes(self, request, pk=None):
    #     notes = self.get_object().notes.filter(owner=self.request.user).all()
    #     return Response(NoteSerializer(notes, many=True).data)
