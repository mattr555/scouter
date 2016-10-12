from django.db import models


class Team(models.Model):
    license = models.CharField(max_length=10, unique=True, primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.license


class Note(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='notes')
    team = models.ForeignKey(Team, related_name='notes')
    body = models.TextField()
