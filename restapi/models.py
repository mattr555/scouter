from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .validators import robot_field_validator
import json


class JSONField(models.TextField):
    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return json.loads(value)

    def to_python(self, value):
        if isinstance(value, dict) or isinstance(value, list):
            return value
        if value is None:
            return value
        return json.loads(value)

    def get_prep_value(self, value):
        return json.dumps(value)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)


class Team(models.Model):
    license = models.CharField(max_length=10, unique=True, primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.license

    def save(self, *args, **kwargs):
        self.license = self.license.upper()
        super(Team, self).save(*args, **kwargs)


class Note(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='notes', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name='notes', on_delete=models.CASCADE)
    body = models.TextField()

class UserProfile(models.Model):
    def default_robot_fields():
        return [
            {"name": "Drive", "type": "option", "options": ["x-drive", "tank", "omni", "h-drive"]},
            {"name": "Handling", "type": "badgood"},
            {"name": "Auto score", "type": "number"}
        ]

    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    robot_fields = JSONField(blank=True, default=default_robot_fields, validators=[robot_field_validator])

    def __str__(self):
        return self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
