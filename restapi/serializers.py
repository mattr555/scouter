from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Note, Team



class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Note
        fields = ('id', 'body', 'created', 'owner', 'team')


class UpperCaseField(serializers.CharField):
    def to_internal_value(self, data):
        ret = super(UpperCaseField, self).to_internal_value(data)
        return ret.upper()

class TeamSerializer(serializers.ModelSerializer):
    # notes = NoteSerializer(many=True, read_only=True)
    notes = serializers.SerializerMethodField()
    license = UpperCaseField(validators=[UniqueValidator(queryset=Team.objects.all(), message="This team already exists.")])

    class Meta:
        model = Team
        fields = ('license', 'name', 'notes')

    def get_notes(self, obj):
        user = self.context['request'].user
        qs = Note.objects.filter(owner=user, team=obj)
        return NoteSerializer(qs, many=True).data

class UserSerializer(serializers.ModelSerializer):
    # notes = serializers.PrimaryKeyRelatedField(many=True, queryset=Note.objects.all())
    # notes = NoteSerializer(many=True, read_only=True)
    # notes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email')

    # def get_notes(self, obj):
    #     user = self.context['request'].user
    #     qs = Note.objects.filter(owner=user)
    #     return NoteSerializer(qs, many=True).data
