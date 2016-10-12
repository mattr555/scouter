from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from restapi import views

router = routers.DefaultRouter()
router.register(r'notes', views.NoteViewSet, base_name="note")
router.register(r'teams', views.TeamViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider'))
]
