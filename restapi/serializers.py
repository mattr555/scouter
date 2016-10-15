from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Note, Team, UserProfile
from .validators import robot_field_validator


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

PROFILE_FIELDS = ('robot_fields',)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    robot_fields = serializers.ListField(source='profile.robot_fields')

    class Meta:
        model = User
        fields = ('id', 'username', 'robot_fields')
        read_only_fields = ('username',)

    #http://stackoverflow.com/a/28733782
    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = super(UserSerializer, self).create(validated_data)
        self.create_or_update_profile(user, profile_data)
        return user

    def update(self, instance, validated_data):
        print(validated_data)
        profile_data = validated_data.pop('profile', None)
        self.create_or_update_profile(instance, profile_data)
        return super(UserSerializer, self).update(instance, validated_data)

    def create_or_update_profile(self, user, profile_data):
        profile, created = UserProfile.objects.get_or_create(user=user, defaults=profile_data)
        if not created and profile_data is not None:
            # super(UserSerializer, self).update(profile, profile_data)
            for attr, val in profile_data.items():
                setattr(profile, attr, val)
            profile.save()

    def validate_robot_fields(self, value):
        robot_field_validator(value)
        return value
